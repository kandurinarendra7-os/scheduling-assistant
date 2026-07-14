# Deployment Guide

This guide covers deploying the Multi-Agent Scheduling Assistant to various platforms.

## Streamlit Cloud (Recommended)

### Steps:
1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repository
   - Set the main file path to `streamlit_app.py`

3. **Add Secrets**
   - In Streamlit Cloud dashboard, go to "Secrets"
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY = "sk-your-key-here"
     ```

4. **Deploy**
   - Click "Deploy"
   - Your app will be live at `https://<username>-<repo>-<random>.streamlit.app`

## Render

### Steps:
1. **Create a new Web Service**
   - Go to https://render.com
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository

2. **Configure**
   - **Name**: scheduling-assistant
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port=10000 --server.address=0.0.0.0`

3. **Add Environment Variables**
   - Go to "Environment"
   - Add `OPENAI_API_KEY` with your API key

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

## Hugging Face Spaces

### Steps:
1. **Create a new Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Streamlit" as the Space SDK
   - Set visibility to "Public"

2. **Upload Files**
   - Upload all project files to the Space
   - Or connect your GitHub repository

3. **Add Secrets**
   - Go to Space settings
   - Add `OPENAI_API_KEY` under "Repository secrets"

4. **Deploy**
   - The Space will automatically build and deploy

## Heroku (Legacy)

### Steps:
1. **Create Procfile**
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create requirements.txt** (already done)

3. **Deploy**
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY="sk-your-key-here"
   git push heroku main
   ```

## Local Development

### Setup:
```bash
# Clone repository
git clone <repository-url>
cd scheduling_assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run app
streamlit run streamlit_app.py
```

## Environment Variables

### Required:
- `OPENAI_API_KEY`: Your OpenAI API key

### Optional:
- `STREAMLIT_SERVER_PORT`: Port number (default: 8501)
- `STREAMLIT_SERVER_HEADLESS`: Set to true for headless mode

## Monitoring & Logs

### Streamlit Cloud:
- View logs in the dashboard
- Monitor app health and usage

### Render:
- View logs in the "Logs" tab
- Monitor CPU and memory usage

### Hugging Face:
- View logs in the Space settings
- Monitor app status

## Troubleshooting

### App crashes on startup:
- Check that all dependencies are installed
- Verify `OPENAI_API_KEY` is set correctly
- Check Python version compatibility

### Slow response times:
- Consider upgrading to a faster LLM model
- Check API rate limits
- Optimize agent prompts

### Memory issues:
- Increase server memory allocation
- Implement conversation cleanup
- Use persistent database instead of in-memory storage

## Cost Optimization

1. **Use cheaper models**: `gpt-4o-mini` instead of `gpt-4`
2. **Implement caching**: Cache common responses
3. **Batch requests**: Combine multiple queries
4. **Monitor usage**: Set up billing alerts

## Security Best Practices

1. **Never commit secrets**: Use `.env` and `.gitignore`
2. **Use environment variables**: For all sensitive data
3. **Validate user input**: Sanitize all user inputs
4. **Rate limiting**: Implement rate limiting for API calls
5. **HTTPS only**: Ensure all connections are encrypted

## Scaling

For production deployments:

1. **Database**: Replace SQLite with PostgreSQL or MongoDB
2. **Caching**: Add Redis for response caching
3. **Load balancing**: Use multiple instances with load balancer
4. **API Gateway**: Add API gateway for rate limiting and authentication
5. **Monitoring**: Implement comprehensive logging and monitoring

---

For more information, refer to the README.md file.
