---
title: Tech Stack Advisor
emoji: 💻
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Tech Stack Advisor 🚀

An automated, enterprise-grade AI application pipeline that deploys a Streamlit interface powered by Google Gemini to Hugging Face Spaces using GitHub Actions.

---

## Architecture Overview

This project uses a Continuous Integration & Continuous Deployment (CI/CD) pipeline to automate infrastructure delivery:
1. Local Workstation (VS Code): Development environment using Python virtual environments (.venv).
2. GitHub Repository: Central source control hosting code, managing security workflows, and scanning for exposed secrets.
3. GitHub Actions: The CI/CD engine that securely triggers on every code push to mirror files to the deployment platform.
4. Hugging Face Spaces (Docker): The production cloud host that builds an isolated container image from a Dockerfile and runs the public frontend.

---

## Prerequisites

Before getting started, make sure you have:
* Python 3.9+ installed locally.
* A GitHub account.
* A Hugging Face account.
* A Google AI Studio API Key (for Gemini model access).

---

## Setup & Deployment Guide

Follow these steps to replicate this architecture from scratch:

### 1. Local Project Initialization

Create your requirements.txt file and add these lines:
streamlit
google-genai

Create your Dockerfile and add these lines:
FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port", "7860", "--server.address", "0.0.0.0"]

Create your .gitignore file and add these lines:
.env
.venv/
__pycache__/

### 2. Configure the Cloud Infrastructure

1. Go to Hugging Face, click New Space, choose Docker as the SDK, and select a blank template.
2. Go to your Space Settings, scroll down to Variables and secrets, and add a New secret:
   * Key: GOOGLE_API_KEY
   * Value: Your Gemini API Key
3. Generate a Hugging Face token with Write access by navigating to your Profile Settings -> Access Tokens.

### 3. Connect GitHub Actions Automation

1. Create a repository on GitHub.
2. Go to your repository Settings -> Secrets and variables -> Actions -> New repository secret:
   * Name: HF_TOKEN
   * Value: Your Hugging Face Write Access Token
3. Define your deployment workflow by creating a file at .github/workflows/sync.yml with these exact contents:

name: Sync to Hugging Face Hub
on:
  push:
    branches: [main]
  force_push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          lfs: true
      - name: Push to Hub
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: git push --force https://mesi-dev:$HF_TOKEN@huggingface.co/spaces/mesi-dev/tech-stack-advisor main

(Note: Remember to replace mesi-dev/tech-stack-advisor with your actual Hugging Face username and Space name).

### 4. Push Code to Launch

Initialize your local git repository, link it to your GitHub remote destination, and trigger the automation by running these terminal commands:

git init
git add .
git commit -m "feat: initial pipeline setup"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main

---

## The Developer Workflow

Once setup is complete, your workflow is entirely streamlined:

1. Write or update code locally inside VS Code.
2. Commit and push your modifications to GitHub:
   git add .
   git commit -m "feat: enhance prompt logic"
   git push origin main
3. GitHub Actions will intercept the push and automatically update your live Hugging Face production app container within seconds.