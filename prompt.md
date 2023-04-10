You are a developer for a startup that is developing a new AI-powered web application. The application will be a clone of the popular ChatGPT Web application, which is an advanced AI-powered web application that can generate high-quality human-like text based on user prompts. The web application is designed to cater to a wide range of use cases, including but not limited to, content generation, information extraction, question-answering, and conversational assistance. The startup has hired you to develop the web application. You have been tasked with developing the front-end and back-end of the web application. You have been given the following requirements for the web application:

ChatGPT Web Clone

OVERVIEW
The proposed ChatGPT Web clone should be an advanced AI-powered web application that can generate high-quality human-like text based on user prompts. The web application should be designed to cater to a wide range of use cases, including but not limited to, content generation, information extraction, question-answering, and conversational assistance.

CORE FUNCTIONALITY OF CHATGPT WEB CLONE
"""
1. User Authentication
The ChatGPT Web clone should allow users to create accounts and sign in to access the web application. Users should be able to sign up using their email addresses or social media accounts. The web application should support multi-factor authentication to enhance account security.

2. Text Generation
The ChatGPT Web clone must be able to generate coherent, contextually relevant, and grammatically correct responses based on user-provided prompts.

3. Conversation History
The web application should allow users to save their conversations for future reference. Users should be able to access saved conversations from the sidebar and export them in various formats.

4. Conversation Editing
The ChatGPT Web clone should allow users to adjust parameters like response length, creativity, and formality to suit their specific needs.

5. Conversation Search
The web application must feature an intuitive, easy-to-use, and visually appealing user interface to facilitate seamless user interaction with the AI model.
"""

TASKS FOR FRONT-END AND BACK-END DEVELOPERS:

FRONT-END DEVELOPMENT TASKS:
"""
1. Develop the main dashboard, featuring:
   - A collapsible sidebar with sections for Conversations, Settings.
   - A "New Conversation" button at the top of the sidebar.
   - A chat window occupying the remaining screen space.

2. Design the chat window, including:
   - A chat area displaying conversation history with alternating message bubbles.
   - An input field for user prompts with a "Send" button or "Enter" key functionality.
   - Buttons or sliders for adjusting AI output parameters.
   - A loading indicator for AI-generated responses.

3. Implement a feature to access saved conversations from the sidebar and provide the option to export conversations in various formats.
"""

BACK-END DEVELOPMENT TASKS:
"""
1. Implement user authentication, including sign-up, login, password recovery, and multi-factor authentication.

2. Set up API calls to the AI model for generating responses based on user prompts and output parameters.

3. Develop a function to fetch and display the selected conversation, allowing users to continue chatting seamlessly.

4. Implement a function to delete an entire conversation with a confirmation prompt.

5. Create a function to delete individual messages within a conversation, with a confirmation prompt.

6. Develop a function to edit user prompts within a conversation, triggering the AI to generate new responses based on the edited input.

7. Ensure automatic saving of conversation progress at regular intervals or after each interaction.

8. Implement a search feature to allow users to find specific conversations by keywords or conversation labels.

9. Develop user account management features, such as updating email addresses, changing passwords, and setting up multi-factor authentication.

10. Ensure data security and privacy by encrypting user data, securely storing conversation history, and adhering to relevant privacy regulations and guidelines.

11. Create a function to export conversations in various formats, such as PDF, CSV, and JSON.
"""

DESIGN REQUIREMENTS
"""
1. User Interface (UI)
1.1. Minimalist Design
The ChatGPT Web clone should feature a clean, minimalist design that emphasizes simplicity and ease of use. The interface should prioritize essential elements and minimize distractions, using whitespace strategically to separate content areas.

1.2. Responsive Design
The web application must be responsive, ensuring a consistent user experience across various screen sizes, devices, and platforms.

1.3. Color Scheme
A visually appealing color scheme should be employed to create a cohesive aesthetic throughout the application. Colors should be chosen for their accessibility, contrast, and relevance to the application’s overall theme.

1.4. Typography
Typography should be clear and legible, with appropriate font choices, sizes, and weights that maximize readability across various devices and screen resolutions.

2. User Experience (UX)
2.1. Intuitive Navigation
The web application should provide a clear, straightforward navigation structure that enables users to access all essential features with minimal effort. Navigation options, such as menus and buttons, should be easily identifiable and consistent throughout the application.
"""