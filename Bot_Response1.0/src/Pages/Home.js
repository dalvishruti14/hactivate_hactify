import React from 'react';
import '../Styles/Home.css'

const Home = () => {
    return (
        <div>


    <div class="welcome-section">
        <div class="robot-container">
            <img src="robot.jpg" alt="Waving Robot"/>
            <p class="robot-text">Hello, I'm your BotTeacher!</p>
        </div>
        <div class="subject-options">
            <h2>Choose a Subject</h2>
            <ul>
                <li><a href="#">English</a></li>
                <li><a href="#">Mathematics</a></li>
                <li><a href="/geography">Geography</a></li>
            </ul>
        </div>
    </div>
        </div>
    );
};

export default Home;
