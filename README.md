# Insta-Motion

## Overview
Welcome to _**Insta-Motion**_! _**Insta-Motion**_ is a _**Sentiment Analyzer**_ designed to Analyze _**Instagram Post Sentiments**_. Whether you are a developer or contributor, this _**README.md**_ will guide you through the essentials of the project.

## Table of Content
1. [Introduction](#introduction)
2. [Application UI](#application-ui)
3. [Getting Started](#getting-started)
4. [Installation](#installation)
5. [Contribution](#contribution)

## Introduction
Your go-to tool for understanding the emotions behind Instagram posts. With just a few clicks, you can explore the sentiment of various posts, uncover trends, and gain insights into how people feel about different topics.

## Application UI
![Screenshot 2024-10-14 125453](https://github.com/user-attachments/assets/de0721a3-71c6-44a0-8968-2ee0aa4e0c98)
![Screenshot 2024-10-14 125529](https://github.com/user-attachments/assets/5eb31869-1f4f-4069-a700-92511da5b8ff)

## Getting Started
Before diving into the project, ensure you have the following prerequisites:
- Programming Language: [Python 3.X](https://www.python.org/)
- Package Manager: [pip](https://pypi.org/project/pip/)
- Version Control: [Git](https://git-scm.com/)
- Integrated Development Environment: [Visual Studio Code](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm)

## Installation
1. Clone Repository
   ```bash
   git clone https://github.com/Arko-Sengupta/Insta-Motions.git
   ```

2. Navigate to the Project Directory
   ```bash
   cd/<Project-Directory>
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Start Backend Server
   ```bash
   python SentimentAnalysis_API.py
   ```

5. Start the Application
   ```bash
   streamlit run App.py
   ```

6. Refer to the below format for `Posts Excel Sheet`
   ```bash
   posts = [
    {
        "Post_ID": "B1abc123",
        "Post_Text": "Having a Good Day!",
        "Post_Date": "2024-09-10",
        "Likes_Count": 123,
        "Comments_Count": 12,
        "Comments": ["Beautiful!", "So lovely!"],
        "Image_URL": "https://image1.jpg",
        "Post_URL": "https://www.instagram.com/p/B1abc123/"
    },
    {
        "Post_ID": "B2def456",
        "Post_Text": "Love this moment!",
        "Post_Date": "2024-09-12",
        "Likes_Count": 456,
        "Comments_Count": 34,
        "Comments": ["Awesome!", "Wow!"],
        "Image_URL": "https://image2.jpg",
        "Post_URL": "https://www.instagram.com/p/B2def456/"
    },
    {
        "Post_ID": "B3ghi789",
        "Post_Text": "Throwback to last summer.",
        "Post_Date": "2024-09-14",
        "Likes_Count": 789,
        "Comments_Count": 56,
        "Comments": ["Great shot!", "Memories!"],
        "Image_URL": "https://image3.jpg",
        "Post_URL": "https://www.instagram.com/p/B3ghi789/"
    }
   ]
   ```

## Contribution
If you'd like to contribute, follow the guidelines
- Create a branch using the format `Insta-Motion_<YourUsername>` when contributing to the project.
- Add the label `Contributor` to your contributions to distinguish them within the project.
