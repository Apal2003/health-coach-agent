import os
import streamlit as st
from typing import List
from dotenv import load_dotenv
import random

load_dotenv()

class HealthCoachAgent:
    def __init__(self):
        # Demo mode - no API key needed
        self.demo_mode = True
        
    def get_recommendations(self, health_summary: str, user_query: str = None) -> str:
        """Get personalized health recommendations (Demo Mode)"""
        
        # Parse the health summary for personalization
        recommendations = []
        
        if "sleep" in user_query.lower() if user_query else False:
            recommendations = [
                "🛏️ **Establish a Consistent Sleep Schedule**: Try going to bed and waking up at the same time every day, even on weekends. This helps regulate your body's internal clock.",
                "📱 **Limit Screen Time Before Bed**: Avoid phones, tablets, and computers at least 1 hour before sleep. The blue light can interfere with melatonin production.",
                "🌡️ **Optimize Your Sleep Environment**: Keep your bedroom cool (60-67°F), dark, and quiet. Consider using blackout curtains or a white noise machine.",
                "☕ **Watch Caffeine Intake**: Avoid caffeine after 2 PM as it can stay in your system for 6-8 hours.",
                "🧘 **Try Relaxation Techniques**: Practice deep breathing, meditation, or gentle stretching before bed to help your body wind down."
            ]
        elif "exercise" in user_query.lower() if user_query else False:
            recommendations = [
                "🚶 **Start with Walking**: Aim for 30 minutes of brisk walking daily. It's low-impact and great for cardiovascular health.",
                "💪 **Add Strength Training**: Include 2-3 sessions of bodyweight exercises (squats, push-ups, planks) per week to build muscle and bone density.",
                "🏃 **Try Interval Training**: Alternate between high and low intensity for better results in less time (e.g., 1 minute fast, 2 minutes slow).",
                "🧘 **Include Flexibility Work**: Add yoga or stretching 2-3 times per week to improve mobility and prevent injury.",
                "⏰ **Schedule It**: Treat exercise like an important appointment. Pick a consistent time that works for your schedule."
            ]
        elif "stress" in user_query.lower() if user_query else False:
            recommendations = [
                "🧘 **Practice Daily Meditation**: Start with just 5 minutes of mindfulness meditation each morning to center yourself.",
                "📝 **Keep a Stress Journal**: Write down what's causing stress and your thoughts. This helps identify patterns and solutions.",
                "🌳 **Spend Time in Nature**: Even 20 minutes outside can significantly reduce cortisol levels and improve mood.",
                "👥 **Connect with Others**: Talk to friends, family, or a therapist. Social support is crucial for managing stress.",
                "⏸️ **Take Regular Breaks**: Use the Pomodoro Technique - work for 25 minutes, then take a 5-minute break."
            ]
        elif "water" in user_query.lower() if user_query else False:
            recommendations = [
                "💧 **Set Hourly Reminders**: Use your phone to remind you to drink water every hour during waking hours.",
                "🥤 **Start Your Day with Water**: Drink a full glass of water immediately upon waking to rehydrate after sleep.",
                "🍋 **Make It Tasty**: Add lemon, cucumber, or mint to make water more appealing if you find it boring.",
                "📊 **Track Your Intake**: Use a water tracking app or a marked water bottle to visualize your progress.",
                "🍽️ **Drink Before Meals**: Have a glass of water 30 minutes before each meal to stay hydrated and aid digestion."
            ]
        elif "diabetes" in health_summary.lower():
            recommendations = [
                "🥗 **Focus on Low Glycemic Foods**: Choose whole grains, vegetables, and lean proteins that won't spike blood sugar.",
                "📊 **Monitor Blood Sugar Regularly**: Keep a log of your readings to identify patterns and adjust your diet/medication accordingly.",
                "🚶 **Exercise After Meals**: A 15-minute walk after eating can help regulate blood sugar levels.",
                "🍽️ **Eat Smaller, Frequent Meals**: This helps prevent blood sugar spikes and keeps energy levels stable.",
                "💊 **Stay Consistent with Medication**: Take medications at the same time daily and never skip doses."
            ]
        else:
            # General wellness recommendations
            recommendations = [
                "💧 **Hydration Goal**: You're averaging good water intake, but aim for 2.5-3L daily, especially on exercise days.",
                "😴 **Sleep Optimization**: Your sleep patterns show some variability. Try to maintain 7-8 hours consistently each night.",
                "🏃 **Exercise Consistency**: Great job on staying active! Consider adding one more day of varied activity to prevent plateaus.",
                "🧘 **Stress Management**: Your stress levels are moderate. Try incorporating 10 minutes of meditation or deep breathing daily.",
                "🥗 **Nutrition Focus**: Track your meals for a week to ensure you're getting balanced nutrients - plenty of vegetables, lean proteins, and whole grains."
            ]
        
        # Return formatted recommendations
        response = "Based on your health data, here are personalized recommendations:\n\n"
        response += "\n\n".join(recommendations[:5])
        response += "\n\n💡 **Remember**: Small, consistent changes lead to lasting results. Pick 1-2 recommendations to focus on this week!"
        
        return response
    
    def analyze_trends(self, wellness_data: List[dict]) -> dict:
        """Analyze wellness trends over time"""
        if not wellness_data:
            return {}
        
        trends = {
            'sleep_trend': self._calculate_trend([d['sleep_hours'] for d in wellness_data]),
            'exercise_trend': self._calculate_trend([d['exercise_minutes'] for d in wellness_data]),
            'stress_trend': self._calculate_trend([d['stress_level'] for d in wellness_data])
        }
        return trends
    
    @staticmethod
    def _calculate_trend(values: List[float]) -> str:
        """Simple trend calculation"""
        if len(values) < 2:
            return "insufficient data"
        
        recent = sum(values[-3:]) / 3 if len(values) >= 3 else values[-1]
        older = sum(values[:3]) / 3 if len(values) >= 3 else values[0]
        
        if recent > older * 1.1:
            return "📈 improving"
        elif recent < older * 0.9:
            return "📉 declining"
        else:
            return "➡️ stable"