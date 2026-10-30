# Template Injection – Cybersecurity 1x0

## 1. Project Overview

This project focuses on discovering and understanding Server-Side Template Injection (SSTI) vulnerabilities in a vulnerable web application.

The application was built using Flask and Jinja2. The main objective was to identify the vulnerability and demonstrate its impact by displaying the contents of the `/etc/passwd` file.

## 2. What is Server-Side Template Injection (SSTI)?

Server-Side Template Injection (SSTI) is a web application vulnerability that occurs when user-controlled input is inserted into a server-side template and interpreted as template code.

Instead of treating user input as ordinary text, the template engine evaluates the injected expressions.

This can expose sensitive information and, depending on the configuration and permissions, may lead to more serious consequences such as Remote Code Execution (RCE).

## 3. Application Analysis

The application uses the following technologies:

- Flask 2.0.1
- Jinja2 3.0.1
- Werkzeug 2.0.1
- Docker

Jinja2 is the template engine responsible for processing template expressions.

During source code analysis, the following code was identified as the vulnerable implementation:

```python
template = f'Hello, {{ {user_input} }}!'
result = render_template_string(template)
```

The application inserts user-controlled input into a dynamically generated template and processes it using `render_template_string()`.

This unsafe implementation is the root cause of the SSTI vulnerability.

## 4. Vulnerability Discovery

The vulnerability was discovered by testing a mathematical expression:

```text
{{7*7}}
```

The application returned:

```text
49
```

This result demonstrated that the server was evaluating the expression instead of displaying it as plain text.

The test confirmed the presence of Server-Side Template Injection.

## 5. Exploitation Results

The vulnerability was successfully exploited in the local testing environment.

The contents of the following system file were displayed through the vulnerable web application:

```text
/etc/passwd
```

The output included system account information such as:

- root
- daemon
- www-data
- nobody

This demonstrated that the vulnerability could expose information from the server's filesystem.

## 6. Exploitation Scenarios

### Scenario 1: Sensitive File Disclosure

An attacker may exploit SSTI to access sensitive files stored on the server when the application has sufficient permissions.

In this project, access to `/etc/passwd` was successfully demonstrated.

**Potential Impact:**
- Disclosure of system account information.
- Exposure of server environment details.
- Information gathering for further attacks.

### Scenario 2: Remote Code Execution (RCE)

In certain vulnerable configurations, SSTI may allow an attacker to access dangerous objects or functions and execute unauthorized system commands.

The possibility and extent of this impact depend on the template engine, its configuration, and the permissions of the application process.

**Potential Impact:**
- Unauthorized command execution.
- Access to server resources and files.
- Possible compromise of confidentiality, integrity, and availability.

Note: This scenario describes a potential impact of SSTI and is not documented as a separate tested scenario in this project.

## 7. Conclusion

This project demonstrated how unsafe handling of user input in server-side templates can introduce serious security vulnerabilities.

By analyzing the application source code and testing the input field, SSTI was identified and successfully demonstrated.

The project highlights the importance of secure template handling, input validation, and following secure development practices to prevent template injection attacks.
