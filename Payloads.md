# Server-Side Template Injection (SSTI) – Payloads Documentation

## 1. Introduction

This document describes the payloads used to identify and demonstrate the Server-Side Template Injection (SSTI) vulnerability in the provided Flask application.

The application uses the Jinja2 template engine to process user input. When user-controlled input is inserted directly into a template and evaluated, an attacker may be able to execute template expressions on the server.

The purpose of these tests is to identify the vulnerability, understand its behavior, and demonstrate its potential security impact in the local educational environment.

---

## 2. Target Application

**Application:** Template Injection App

**Framework:** Flask

**Template Engine:** Jinja2

**Vulnerable Function:** `render()`

**Endpoint:** `/render`

**HTTP Method:** POST

**Vulnerable Code:**

```python
user_input = request.form.get('input')
template = f'Hello, {{ {user_input} }}!'
result = render_template_string(template)
```

### Why Is This Code Vulnerable?

The application directly inserts user-controlled input into a template string and then passes that string to `render_template_string()`.

As a result, Jinja2 interprets the supplied input as template code instead of treating it as ordinary text.

This behavior creates a Server-Side Template Injection vulnerability.

---

## 3. Payload 1 – Basic Template Expression Test

**Payload:**

```jinja2
{{7*7}}
```

**Purpose:**

To determine whether the application evaluates user input as a server-side template expression.

**Expected Behavior:**

If the application evaluates the expression, the mathematical operation will be calculated by the template engine.

**Observed Result:**

The application returned:

```text
Hello, { 49 }!
```

**Analysis:**

The result `49` confirms that Jinja2 evaluated the supplied expression.

This is the first indication that the application is vulnerable to SSTI.

**Status:** Successfully tested.

---

## 4. Payload 2 – String Expression Test

**Payload:**

```jinja2
{{'Hello'}}
```

**Purpose:**

To test whether Jinja2 evaluates string expressions supplied through the input field.

**Expected Behavior:**

The template engine should evaluate the expression and return the string value.

**Security Significance:**

Successful evaluation of template expressions indicates that user input is being interpreted by the server-side template engine.

**Status:** Additional test example; not separately documented as tested.

---

## 5. Payload 3 – Sensitive File Disclosure

**Payload:**

```jinja2
{{ cycler.__init__.__globals__.os.popen('cat /etc/passwd').read() }}
```

**Purpose:**

To demonstrate the possibility of accessing sensitive files through the vulnerable template engine.

**Explanation:**

- `cycler` accesses a Jinja2 global object.
- `__init__` accesses its initialization method.
- `__globals__` accesses the global namespace.
- `os.popen()` executes a system command.
- `cat /etc/passwd` reads the specified system file.
- `.read()` retrieves the command output.

**Observed Result:**

The application successfully displayed the contents of:

```text
/etc/passwd
```

**Analysis:**

This confirms that the vulnerability allowed access to sensitive server-side file information in the local lab environment.

The result demonstrates a serious security impact beyond simple template expression evaluation.

**Status:** Successfully tested.

---

## 6. Payload Execution Results

| Payload | Purpose | Result |
|---|---|---|
| `{{7*7}}` | Detect template evaluation | Successfully returned 49 |
| `{{'Hello'}}` | Test string expression evaluation | Additional example, not separately tested |
| File disclosure payload | Read `/etc/passwd` | Successfully displayed file contents |

---

## 7. Exploitation Scenarios

### Scenario 1 – Sensitive File Disclosure

An attacker may exploit SSTI to access sensitive files stored on the server when the application and template environment allow such access.

In this project, the `/etc/passwd` file was successfully accessed through the vulnerable input field.

**Potential Impact:**

- Disclosure of system account information.
- Exposure of server environment details.
- Information gathering for further attacks.
- Increased risk of additional security compromises.

**Testing Status:** Successfully demonstrated.

### Scenario 2 – Remote Code Execution (RCE)

In certain vulnerable template configurations, SSTI may allow an attacker to access dangerous objects or functions and execute unauthorized operating system commands.

The possibility and extent of this impact depend on the template engine, its configuration, available objects, and the permissions of the application process.

**Potential Impact:**

- Unauthorized command execution.
- Access to server resources and files.
- Possible compromise of confidentiality, integrity, and availability.

**Testing Status:** Documented as a potential impact, not as a separate tested scenario in this project.

---

## 8. Security Risks

Server-Side Template Injection can lead to several security problems, depending on the application's configuration and permissions.

The main risks include:

1. Unauthorized template expression evaluation.
2. Disclosure of sensitive server-side information.
3. Unauthorized access to files.
4. Potential operating system command execution.
5. Possible compromise of application and server security.

---

## 9. Recommendations

To prevent SSTI vulnerabilities:

- Never construct templates directly from untrusted user input.
- Use fixed and trusted templates.
- Pass user input as template variables instead of inserting it into template source code.
- Apply input validation where appropriate.
- Restrict application permissions.
- Avoid exposing unnecessary objects and functions to templates.
- Keep Flask and Jinja2 dependencies updated.
- Follow secure development practices.

---

## 10. Conclusion

The tests performed in this project demonstrated a Server-Side Template Injection vulnerability in the provided Flask application.

The basic expression payload confirmed that user input was evaluated by Jinja2.

The file disclosure payload demonstrated that the vulnerability could be exploited to access the contents of `/etc/passwd` in the local educational environment.

These results highlight the importance of secure template handling and the risks of directly evaluating user-controlled input.

All testing was performed within the provided local educational environment for cybersecurity learning purposes.
