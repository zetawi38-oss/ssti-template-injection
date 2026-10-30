# Server-Side Template Injection (SSTI) – Security Fixes

## 1. Introduction

This document explains the security measures required to prevent Server-Side Template Injection (SSTI) vulnerabilities in the provided Flask application.

The vulnerability occurs because the application inserts user-controlled input directly into a template string and evaluates it using the Jinja2 template engine.

The main objective is to ensure that user input is treated as data rather than executable template code.

---

## 2. Root Cause of the Vulnerability

The vulnerable code is:

```python
user_input = request.form.get('input')
template = f'Hello, {{ {user_input} }}!'
result = render_template_string(template)
```

### Why Is It Dangerous?

The application creates a template using an f-string that contains untrusted user input.

It then passes the generated template to `render_template_string()`.

Because Jinja2 processes the resulting string as template source code, an attacker may inject template expressions that are evaluated on the server.

This can lead to sensitive information disclosure and, under certain configurations, more serious security impacts.

---

## 3. Recommended Fix – Use a Fixed Template

The safest approach is to avoid building template source code using user input.

Instead, use a fixed template and pass user input as a variable.

### Vulnerable Approach

```python
user_input = request.form.get('input')
template = f'Hello, {{ {user_input} }}!'
result = render_template_string(template)
```

### Secure Approach

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/render', methods=['POST'])
def render():
    user_input = request.form.get('input', '')

    template = 'Hello, {{ user_input }}!'

    result = render_template_string(
        template,
        user_input=user_input
    )

    return render_template_string(index(), result=result)
```

### Explanation

- The template source is fixed and controlled by the developer.
- User input is passed as a template variable.
- Jinja2 treats the input as data rather than interpreting it as template source code.
- Expressions supplied by the user are not evaluated as part of the template.

This prevents the original template injection issue.

---

## 4. Additional Security Measures

### 4.1 Avoid Dynamic Template Construction

Never concatenate or interpolate untrusted user input into template source code.

Use predefined templates and pass user data through template variables.

### 4.2 Validate User Input

Apply input validation based on the application's requirements.

Validation should restrict unexpected input and reject values that do not match the expected format.

Input validation is an additional security measure and should not replace safe template handling.

### 4.3 Apply Least Privilege

Run the Flask application with the minimum permissions required.

Avoid running web applications as the root user.

Restrict access to sensitive files and system resources.

### 4.4 Restrict Access to Sensitive Resources

The application should only have access to the files and resources required for its operation.

Sensitive system files should not be unnecessarily accessible to the application process.

### 4.5 Avoid Exposing Dangerous Objects

Do not expose unnecessary Python objects, functions, or system-related capabilities to template contexts.

Keep the template environment as restricted as possible.

### 4.6 Keep Dependencies Updated

Use supported and updated versions of Flask, Jinja2, and other dependencies.

Monitor security advisories and apply security patches when necessary.

### 4.7 Follow Secure Development Practices

- Review source code before deployment.
- Perform security testing.
- Avoid unsafe handling of user-controlled input.
- Use secure coding standards.
- Review application permissions and configurations.

---

## 5. Verification After Applying the Fix

After implementing the secure approach, the application should be tested again.

### Test 1 – Basic Template Expression

**Input:**

```jinja2
{{7*7}}
```

**Expected Secure Behavior:**

The application should display the input as ordinary user data instead of evaluating the expression.

For example:

```text
Hello, {{7*7}}!
```

The application should not return `49` as the evaluated result.

### Test 2 – Sensitive File Disclosure

**Input:**

A template expression attempting to access `/etc/passwd`.

**Expected Secure Behavior:**

The application should display the submitted text as ordinary data, not execute it.

The contents of `/etc/passwd` should not be returned.

---

## 6. Security Comparison

| Area | Vulnerable Application | Secure Application |
|---|---|---|
| Template construction | Uses user input in template source | Uses a fixed template |
| User input | May be interpreted as template code | Passed as a variable |
| Expression evaluation | User expressions may be evaluated | User expressions remain data |
| File disclosure | Demonstrated in the lab | Prevented by safe template handling |
| Security design | Unsafe input handling | Separation of code and data |

---

## 7. Conclusion

The SSTI vulnerability in the provided application was caused by directly inserting user-controlled input into a server-side template.

The recommended solution is to use predefined templates and pass user input as variables instead of dynamically constructing template source code.

Additional protections include input validation, least-privilege permissions, restricting access to sensitive resources, and keeping dependencies updated.

Applying these measures significantly reduces the risk of Server-Side Template Injection and improves the overall security of the application.

All recommendations are intended for the provided educational project and secure application development.
