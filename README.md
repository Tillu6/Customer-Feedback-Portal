# 🌟 3D Customer Feedback Portal 🚀
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/d55ed8a5-33ac-493b-9db0-5a4a21cdcbf2" />

<div align="center">

![3D Feedback Portal](https://img.shields.io/badge/3D%20Feedback-Portal-blue?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Three.js](https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=three.js&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)

**Experience the future of feedback visualization with stunning 3D graphics! 🎯**

[🌐 Live Demo](https://youtu.be/haYF0aFeNUc) • [📚 Documentation](#api-documentation) • [🚀 Quick Start](#quick-start)

---

### ✨ **Why You'll Love This Project**

🎨 **Beautiful 3D Graphics** • 💡 **Smart AI Analysis** • ⚡ **Lightning Fast** • 📱 **Mobile Ready**

</div>

---

## 🎯 What This Does

Turn boring feedback forms into **amazing 3D experiences**! This portal helps businesses:

- 📊 **Visualize feedback** in stunning 3D charts
- 🧠 **Analyze emotions** automatically with AI
- ⚡ **Get insights** in real-time
- 🎨 **Wow customers** with futuristic design

---

## 🌟 Amazing Features

### 🎨 **Visual Excellence**
- 🌈 **3D Bar Charts** - See your data come alive
- ✨ **Floating Particles** - Beautiful sentiment visualization  
- 🎭 **Futuristic Design** - Gradients, animations, and glow effects
- 📱 **Mobile Perfect** - Works great on all devices

### 🧠 **Smart Features**
- 🤖 **AI Sentiment Analysis** - Knows if feedback is happy or sad
- ⭐ **Star Ratings** - Easy 1-5 star system
- 📊 **Real-time Stats** - Watch numbers update instantly
- 🗂️ **Category Sorting** - Product, Service, Support categories

### ⚡ **Technical Power**
- 🚀 **Super Fast API** - Built with FastAPI
- 💾 **Smart Database** - MongoDB with proper data models
- 🔒 **Data Safe** - UUID-based secure storage
- 🌐 **API Ready** - RESTful endpoints for everything

---

## 🖼️ Screenshots

<div align="center">

### 🏠 **Beautiful Homepage**
*Stunning hero section with data visualization background*
<img width="946" height="375" alt="image" src="https://github.com/user-attachments/assets/fbd2d7c6-2f48-4644-8c77-75f40a7058bf" />


### 📊 **3D Dashboard Magic**
*Watch your feedback data dance in 3D space*
<img width="740" height="326" alt="image" src="https://github.com/user-attachments/assets/d87e256e-2213-4868-8f33-b129d9d20640" />

### 📝 **Smart Feedback Form**
*Easy-to-use form with interactive star ratings*
<img width="815" height="441" alt="image" src="https://github.com/user-attachments/assets/4b2ae36b-a808-46f0-b6a9-32c1643918af" />


</div>

---

## 🛠️ Tech Stack

<div align="center">

| **Frontend** | **Backend** | **Database** | **3D Graphics** |
|--------------|-------------|--------------|----------------|
| ⚛️ React | 🐍 FastAPI | 🍃 MongoDB | 🎮 Three.js |
| 🎨 Tailwind CSS | 🔧 Pydantic | 🏃‍♂️ Motor | 📊 WebGL |
| 📦 Axios | 🌐 CORS | 🔑 UUID | ✨ Animations |

</div>

---

## 🚀 Quick Start

### 📋 **What You Need**
- 🐍 Python 3.8+
- 📦 Node.js 16+
- 🍃 MongoDB
- ❤️ Love for beautiful code

### ⚡ **Super Easy Setup**

1. **📥 Get the code**
```bash
git clone https://github.com/Tillu6/Customer-Feedback-Portal.git
cd Customer-Feedback-Portal
```

2. **🔧 Setup Backend**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MongoDB URL
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

3. **🎨 Setup Frontend**
```bash
cd frontend
yarn install
yarn start
```

4. **🎉 Open & Enjoy!**
```
🌐 Frontend: http://localhost:3000
🔧 Backend: http://localhost:8001
📚 API Docs: http://localhost:8001/docs
```

---

## 📚 API Documentation

### 🎯 **Main Endpoints**

| Method | Endpoint | What It Does | Example |
|--------|----------|--------------|---------|
| 📝 POST | `/api/feedback` | Create new feedback | `{"rating": 5, "comment": "Amazing!"}` |
| 📖 GET | `/api/feedback` | Get all feedback | Returns feedback list |
| 📊 GET | `/api/feedback/stats` | Get 3D chart data | Returns statistics |
| 🗂️ GET | `/api/feedback/category/{cat}` | Filter by category | `product`, `service`, etc. |
| 🗑️ DELETE | `/api/feedback/{id}` | Delete feedback | Removes by ID |

### 📝 **Feedback Object**
```json
{
  "id": "uuid-string",
  "customer_name": "John Doe",
  "customer_email": "john@example.com", 
  "category": "product",
  "rating": 5,
  "comment": "This is amazing!",
  "sentiment_score": 0.8,
  "timestamp": "2025-01-01T12:00:00Z"
}
```

---

## 🎮 How to Use

### 👤 **For Customers**
1. 🌐 Visit the portal
2. 📝 Click "Submit Feedback"
3. ⭐ Rate your experience (1-5 stars)
4. 💬 Write your thoughts
5. ✨ Submit and see the magic!

### 👨‍💼 **For Business Owners**
1. 📊 Check the 3D Dashboard
2. 🎯 Watch live statistics
3. 📈 See rating trends
4. 💡 Make data-driven decisions

---

## 🎨 Customization

### 🌈 **Change Colors**
Edit `/frontend/src/App.css` and modify:
```css
:root {
  --primary-color: #00d4ff;    /* Main blue */
  --secondary-color: #7c3aed;  /* Purple accent */
  --success-color: #10b981;    /* Green for good ratings */
}
```

### 🎮 **Modify 3D Graphics**
Check `/frontend/src/App.js` in the `init3DVisualization()` function:
- 📊 Change bar colors
- ✨ Adjust particle effects  
- 🎭 Modify animations

---

## 🤝 Contributing

We ❤️ contributions! Here's how:

1. 🍴 **Fork** this repo
2. 🌿 **Create** your feature branch (`git checkout -b amazing-feature`)
3. ✨ **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. 📤 **Push** to branch (`git push origin amazing-feature`)
5. 🎉 **Open** a Pull Request

### 🐛 **Found a Bug?**
- 📧 Open an issue with details
- 🏷️ Use proper labels
- 📷 Include screenshots if possible

---

## 📊 Project Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/Tillu6/Customer-Feedback-Portal?style=social)
![GitHub forks](https://img.shields.io/github/forks/Tillu6/Customer-Feedback-Portal?style=social)
![GitHub issues](https://img.shields.io/github/issues/Tillu6/Customer-Feedback-Portal)
![GitHub license](https://img.shields.io/github/license/Tillu6/Customer-Feedback-Porta)

</div>

---

## 🛣️ Roadmap

### 🔥 **Coming Soon**
- [ ] 🤖 **AI-Powered Analysis** with OpenAI
- [ ] 📧 **Email Notifications** for new feedback
- [ ] 🔐 **User Authentication** system
- [ ] 📱 **Mobile App** version
- [ ] 📈 **Advanced Analytics** dashboard
- [ ] 🌍 **Multi-language** support

### 💡 **Ideas Welcome!**
Have cool ideas? Open an issue and let's discuss! 

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR**: You can use this for anything! Just keep the license notice. 😊

---

## 🙏 Thanks

### 💝 **Special Thanks To**
- 🎮 **Three.js** - For amazing 3D graphics
- ⚛️ **React Team** - For the awesome framework  
- 🐍 **FastAPI** - For the lightning-fast backend
- 🍃 **MongoDB** - For reliable data storage
- ❤️ **You!** - For checking out this project

---

## 📞 Contact

<div align="center">

**Questions? Ideas? Just want to say hi? 👋**

[![Email](https://img.shields.io/badge/Email-psakethreddy97@gmail.com-red?style=for-the-badge&logo=gmail)](mailto:psakethreddy97@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Saketh Poreddy-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/saketh-poreddy-145a7315b/)

**Made with ❤️ and lots of ☕**

⭐ **Don't forget to give this repo a star if you liked it!** ⭐

</div>

---

<div align="center">

### 🎯 **Ready to Transform Your Feedback Experience?**

[🚀 **Get Started Now**](#quick-start) • [💬 **Ask Questions**](#contact) • [⭐ **Star This Repo**](../../)

---

*"The best feedback portal in the galaxy!" 🌌*

</div>
