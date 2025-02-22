## **🚀 AI-Powered Content Generation with CrewAI**
An multi-agent system for **AI research, writing, and content optimization** using `crew.ai`. This project automates **end-to-end content creation**, from **trend research to content generation, SEO optimization, and quality assurance**, producing high-quality, structured outputs for blogs, LinkedIn, and social media.  

---

### 🛠️ Installation
Ensure you have **Conda** installed. If you don’t have it, download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

#### **Create and Activate a Conda Environment**
```bash
conda create --name crewai-content python=3.12
conda activate crewai-content
```

#### **Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **🚀 Usage**
### **1️⃣ Run the AI Content Creation Pipeline**
Run the script with a custom subject using the command line:
```bash
python crew_pipeline.py --subject "The Future of AI-Driven Decision Making"
```

This will:
1. Monitor **AI trends & research papers** on a specified topic.
2. Generate a **structured blog post** using AI.
3. Optimize for **SEO, readability, and engagement**.
4. Perform **quality assurance & editorial review**.
5. Output **blog content + social media snippets**.


### **2️⃣ View & Save Results**
- **Generated Blog Post** → `generated_content/blog_post.md`
- **Social Media Posts** → `generated_content/social_media_posts.txt`

---

## **📂 Project Structure**
```
│── config/                         # Configuration files
│   ├── agents.yaml                 # AI agent configurations (roles, goals, backstories)
│   ├── tasks.yaml                  # Definitions of tasks for each AI agent
│── crewai_content_creation.py      # Main notebook to run the AI-powered content generation pipeline
│── helpers.py                       # Helper script to load env variables with OpenAI API key or other scripts in the future
│── requirements.txt                # Dependencies for the project
│── README.md                       # Project documentation
```

---

## **🛠️ Customization**
### **Modify the AI Agents**
Edit `agents.yaml` to adjust **agent roles, responsibilities, and tool access**.  

### **Adjust Content Workflow**
Modify `tasks.yaml` to **add, remove, or tweak** tasks in the content pipeline.  

---

## **📌 Example Output**
After running the pipeline, you’ll get:
✅ **Blog Post (Markdown)**  
✅ **Key Takeaways & References**  
✅ **Social Media Posts (LinkedIn, Twitter, etc.)**  

```
{
  "title": "The Future of Work: AI Agents and Automation",
  "summary": "AI agents are redefining workflows, automating routine tasks, and enabling human-machine collaboration...",
  "article": "## The Future of Work: AI Agents and Automation...\n\n(Full blog content here)...",
  "key_takeaways": ["AI agents are automating workflows...", "Human oversight remains essential..."],
  "references": ["https://arxiv.org/abs/2405.07437", "https://huggingface.co/blog/open-deep-research"],
  "social_media_posts": [
    {"platform": "LinkedIn", "content": "AI agents are redefining work... #FutureOfWork"},
    {"platform": "Twitter", "content": "The future of work is AI-driven! 🚀 Read more: [link]"}
  ]
}
```
---

## **👥 Connect & Follow**
Follow along for updates and discussions!  

📌 **LinkedIn:** [Bruno Janota](https://www.linkedin.com/in/bjanota/)  
📌 **Blog Post:** [Coming Soon]  