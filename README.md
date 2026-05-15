
## Introduction

Welcome to Money Map, a comprehensive web application designed to help users efficiently manage their personal finances. This platform enables users to track their income, expenses, and budgets, providing insightful reports and visualizations to support better financial decision-making. Built with Django, Money Map offers a user-friendly interface and robust functionality for both casual users and those seeking advanced budgeting tools.

Money Map features a fully responsive design, ensuring seamless usability across desktops, tablets, and smartphones. The site is fantasy map themed, allowing you to “map” your expenses and budgets in a visually engaging way. More details on the theme will be added soon.

## Live Links: 

https://money-map-422d80e8e44a.herokuapp.com/

## Features

- **User Authentication**: Secure signup, login, and logout functionality to protect user data and personalize the experience.
- **Dashboard**: An overview of your financial status, including recent expenses, budget summaries, and quick access to key actions.
- **Expense Tracking**: Add, edit, and delete expenses with support for categories, dates, and descriptions. Easily manage your spending history.
- **Budget Management**: Create and manage budgets for different categories. Set monthly limits and monitor your progress.
- **Category Reports**: Generate detailed reports by category to analyze spending patterns and identify areas for improvement.
- **Monthly Reports**: View monthly summaries of your income and expenses, including visual charts for easy interpretation.
- **Account Management**: Update your account information and manage your profile securely.
- **Responsive Design**: The site is optimized for both desktop and mobile devices, ensuring accessibility anywhere.
- **Fantasy Map Theme**: Visualize your financial journey as a map, making expense tracking more engaging and intuitive. (More to come!)
- **Data Backup**: Safeguard your financial data with backup options.
- **Admin Panel**: For site administrators, manage users, categories, and expenses from a dedicated admin interface.

Money Map is designed to make financial tracking simple, insightful, and secure. Whether you want to monitor daily spending or plan for long-term goals, this site provides all the tools you need.

## Project Diagram

<img src="images/Diagram.png" width="300" alt="Project Diagram" />

The project diagram provides a high-level overview of the application's architecture and main components. It illustrates how different modules interact to deliver a seamless expense tracking experience.


## Wireframes


### Wireframes
<div style="display: flex; gap: 20px; align-items: flex-start;">
	<div>
		<img src="images/Laptop-wireframe.png" width="400" alt="Laptop Wireframe" />
		<p style="text-align:center; font-size:14px;">Laptop Wireframe</p>
	</div>
	<div>
		<img src="images/Mobile-wireframe.png" width="400" alt="Mobile Wireframe" />
		<p style="text-align:center; font-size:14px;">Mobile Wireframe</p>
	</div>
</div>

The wireframes Above demonstrate the layout and user interface for both desktop and mobile users, highlighting the main navigation, dashboard features, and responsive design.


## AI Assistance

AI (GitHub Copilot) was used throughout the development of Money Map to support debugging, optimisation, implementation decisions, and documentation. AI tools acted as a development assistant by helping identify potential issues, suggesting improvements to Django implementation, and accelerating problem-solving. However, all AI-generated suggestions were critically evaluated, tested, and adapted before being implemented to ensure correctness, security, and suitability for the application. Below are some more specific examples of how AI was used to debug and optimise code: 

### AI-Assisted Code Optimisation and Performance Improvements:

AI contributed to improving the efficiency of database queries and data processing logic, particularly in dashboard and reporting features. It recommended replacing manual Python-based aggregation with Django ORM functions such as:

aggregate(Sum('amount'))
annotate(month=TruncMonth('date'))

These improvements reduced unnecessary iteration over querysets and improved performance when calculating totals, monthly breakdowns, and chart data. AI also suggested removing redundant imports and consolidating repeated query logic, which improved code readability and maintainability. These optimisations resulted in cleaner, more efficient, and more scalable database operations.

### Resolving Logout and URL Issues with AI:

During the development of this project, I encountered an issue where the logout button was not functioning as expected. To resolve this, I leveraged AI assistance, which guided me through a systematic debugging process. The AI helped me trace the problem by reviewing the relevant Django views, templates, and URL configurations. It identified inconsistencies in the URL patterns and template links, ensuring that the logout functionality was correctly mapped and accessible. Additionally, the AI assisted in verifying that all authentication-related URLs (login, logout, signup) were properly connected and operational. Through step-by-step troubleshooting, code suggestions, and validation of the changes, the AI enabled me to efficiently debug the issue, resulting in a fully functional logout button and seamless navigation across all authentication routes. This collaborative debugging process not only fixed the immediate problem but also improved the overall reliability of the user authentication flow in the application.

### Debugging Authentication and Access Control Issues:

During testing, a critical security issue was identified where unauthenticated users could access restricted views such as /dashboard/, /add_expense/, and related edit/delete endpoints by directly entering URLs. This bypassed the intended navigation flow and led to a server-side crash (HTTP 500 error). The error occurred because Django attempted to execute database queries using request.user, which returned an AnonymousUser object when no authentication was present. This resulted in invalid ORM filtering, as shown below:

Expense.objects.filter(user=request.user)

Since AnonymousUser cannot be used in database queries expecting a valid user instance, this caused a runtime exception and application failure. AI was used to diagnose this issue in detail. It identified that Django does not automatically protect views unless explicitly secured, meaning that URL-based access bypasses frontend restrictions entirely. It also explained that the root cause was inconsistent application of the @login_required decorator across key views. Specifically, AI highlighted that while some views (such as budget and reporting features) were protected, critical functional views including:

dashboard
add_expense
edit_expense
delete_expense

were missing authentication enforcement, creating a security vulnerability. AI further clarified that this issue was not only a runtime error but also a security flaw, as it allowed unauthorised access attempts to reach sensitive application logic. To resolve the issue, AI guided the implementation of consistent server-side authentication using the @login_required decorator across all restricted views. This ensured that unauthenticated users are redirected to the login page before any database interaction occurs, preventing both application crashes and unauthorised data access. After implementing the fix, direct URL access to protected views correctly redirects users to the login page, and the application no longer attempts to process database queries for unauthenticated sessions.

### AI-Assisted Authentication Migration (Django Allauth):

AI was used to support a significant improvement to the application’s authentication system by migrating from a custom login implementation to Django Allauth. This change was made to improve security, reduce manual authentication handling, and align the project with established Django best practices. Initially, the project used a custom authentication flow, which required manual handling of login templates, URL routing, and session management. This approach increased complexity and introduced potential inconsistencies in authentication handling across the application. AI assisted in identifying that Django Allauth provides a more robust and standardised authentication framework, offering built-in support for login, logout, registration, password management, and session handling.

During the migration process, AI provided step-by-step guidance on:

Removing the existing custom login modal and associated authentication views
Updating urls.py to include Allauth authentication routes
Installing and configuring django-allauth in settings.py
Adjusting installed apps to include required Allauth modules such as:
allauth
allauth.account
allauth.socialaccount (where applicable)
Configuring authentication backends to integrate Allauth with Django’s authentication system
Updating templates to use Allauth’s standard login and signup views

AI also helped ensure that the migration did not break existing application functionality, particularly around session handling and user-specific data access. It highlighted the importance of testing authentication flows after configuration changes to ensure continuity of user experience. After implementation, authentication became more stable, secure, and maintainable. Users were able to log in and log out using a standardised system, and the application benefited from reduced custom authentication code and improved scalability for future features.

### Summary of AI Contribution

Overall, AI played a supportive role in debugging, optimisation, and development decision-making. It helped identify the root causes of authentication errors, improve database query efficiency, and guide best-practice Django implementation.

A key outcome of using AI was improved understanding of Django’s authentication system, particularly the importance of applying server-side access control rather than relying on frontend restrictions alone. All final implementation decisions were verified and tested manually to ensure correctness and reliability.

## Deployment

The application was deployed using Heroku to provide a live production version of Money Map. The deployment process required adapting the project from a local development environment to a cloud-based production environment, including configuration of dependencies, environment variables, and Django production settings.

During initial deployment, several issues were encountered that prevented the application from running correctly. These issues were diagnosed using Heroku logs, which provided detailed runtime error messages. GitHub Copilot (AI) was also used to help interpret these errors and suggest appropriate fixes based on Django and Heroku deployment best practices.

### Deployment Issues and Resolutions
1. Missing pkg_resources module (ModuleNotFoundError)

The application initially failed to start due to a missing Python module: pkg_resources. This occurred because the setuptools package, which provides this module, was not correctly installed in the production environment.

Resolution:
The issue was resolved by adding setuptools and wheel to requirements.txt and ensuring they were correctly installed during deployment. This ensured compatibility between the production environment and project dependencies.

2. Unsupported Python version on Heroku

Heroku initially defaulted to Python 3.14, which was not fully compatible with some project dependencies, including Gunicorn and other supporting libraries.

Resolution:
A runtime.txt file was created to explicitly specify Python 3.12.8, aligning the deployment environment with the local development setup. This ensured consistent behaviour across environments and resolved compatibility issues.

3. DisallowedHost error at runtime

The application returned a DisallowedHost error when accessed via the Heroku URL, indicating that the domain was not correctly configured in Django settings.

Resolution:
The Heroku app domain (money-map-422d80e8e44a.herokuapp.com) was added to the ALLOWED_HOSTS setting in settings.py, allowing Django to accept requests from the deployed environment.

4. Heroku build cache conflicts

Repeated deployment failures occurred due to outdated or conflicting cached dependencies within the Heroku build system.

Resolution:
The build cache was cleared using heroku repo:purge_cache, and the application was redeployed. This ensured that all dependencies were freshly installed and aligned with the updated configuration.


### AI and Debugging Support in Deployment

AI (GitHub Copilot) was used alongside Heroku logs to interpret error messages and suggest possible causes and fixes. This was particularly useful in translating technical deployment errors into actionable solutions, such as identifying missing packages, configuration mismatches, and environment inconsistencies. An example of this during deployment, static files were not initially rendering on the live application. This issue was caused by incomplete WhiteNoise configuration and incorrect middleware ordering. The issue was resolved by adding the appropriate static files storage backend and correctly positioning WhiteNoise in the middleware stack. After redeployment and running collectstatic, all static assets were served correctly.   

Heroku logs provided the primary source of debugging information, while AI assisted in understanding the meaning of error outputs and recommending Django-specific fixes. This combination allowed for efficient resolution of deployment issues and reduced the time required to stabilise the production environment.

### Summary of Deployment Process

Once all issues were resolved, the application successfully deployed to Heroku and functioned as expected in a live environment. Core features such as authentication, budgeting, and expense tracking operated correctly, confirming that the production configuration matched the development setup.

This process highlighted the importance of environment configuration, dependency management, and log-based debugging when deploying Django applications.

## CRUD Functionality

Money Map implements full CRUD (Create, Read, Update, Delete) functionality across its core features:

- **Create**: Users can add new expenses and budgets. The platform provides intuitive forms for entering details such as amount, date, description, and category. Categories are predefined and can be selected, but not created by users.
- **Read**: All financial data can be viewed in dashboards, reports, and lists. Users can browse their expenses and budgets, and generate detailed reports for analysis. Categories are available for selection and reporting.
- **Update**: Existing expenses and budgets can be edited. Users can modify details to correct mistakes or adjust their financial plans as needed. Category management (add/edit/delete) is restricted to administrators via the admin panel.

- **Delete**: Users can remove expenses and budgets that are no longer relevant. Deletion is straightforward and helps keep records organized. Categories cannot be deleted by users; this is managed by administrators.

With these features, Money Map empowers users to manage their finances confidently and efficiently, supporting both everyday tracking and long-term planning. The system is designed to be intuitive and secure, so users can focus on their goals without worrying about data management.


## Notifications

Money Map includes a notification system to enhance user experience and provide feedback. Users are notified each time an action is completed, such as:

- Registration (account creation)
- Login (confirmation of successful login)
- Adding an expense (item created)
- Deleting an expense (item deleted)
- Editing an expense or budget

These notifications confirm successful operations and help users stay informed about changes to their financial data. The notification system ensures clarity and transparency throughout the application, making interactions smooth and reassuring.

## Testing

Manual testing was performed throughout the development of Money Map. All core features—including signup, login, logout, adding, editing, and deleting expenses and budgets—were thoroughly tested by hand. Scrollbars and all interactive elements were checked to ensure proper functionality and usability. Every test passed successfully, confirming that the application works as intended across all supported actions and user flows. The manual test cases were derived from the project user stories and acceptance criteria. Each core feature was tested to confirm that it met the expected functional, usability, responsiveness, and data-handling requirements.
All core test cases passed successfully. Minor issues were identified during testing and were resolved prior to final submission.

AI tools such as GitHub Copilot were used to assist in generating Django unit tests. The generated tests were reviewed and adapted to align with the project’s functionality.

![Testing Screenshot](images/Testing.png)
*Testing Screenshot: Example of test results and UI validation*

All tests passed successfully, confirming that key features behave as expected.

## Validation

HTML and CSS were validated using W3C validation tools.



<div style="display: flex; gap: 32px; align-items: flex-start; margin-bottom: 16px; justify-content: center;">
	<div>
		<img src="images/css.validator.png" width="480" alt="CSS Validator Screenshot" />
		<p style="text-align:center; font-size:14px;">CSS Validator Screenshot</p>
	</div>
	<div>
		<img src="images/html.validator.png" width="480" alt="HTML Validator Screenshot" />
		<p style="text-align:center; font-size:14px;">HTML Validator Screenshot</p>
	</div>
</div>

## Agile Methodology

An Agile approach was used throughout the development of this project. The application was developed in iterative stages, focusing on building core functionality first and then gradually adding additional features.

User stories were used to guide development and ensure that all required features were implemented in a structured and user-focused way. These helped prioritise functionality such as expense tracking, editing, deleting, and reporting.

### Iterative Development

The application was continuously tested and improved throughout development. This iterative process allowed for early identification of issues and ensured that the final application met functional and usability requirements.



## Challenges

During development, an attempt was made to implement a custom authentication system. However, this approach introduced complexity and potential security concerns. 
As a result, the decision was made to refactor the authentication system and integrate Django Allauth instead. This improved reliability, reduced development time, and ensured best practices were followed.
This process was challenging but provided valuable insight into authentication workflows and the importance of using established frameworks.

## Future Improvements

- Add functionality for users to upload images of receipts when recording expenses. This would enhance usability by allowing users to keep visual records of their transactions and improve overall expense tracking.