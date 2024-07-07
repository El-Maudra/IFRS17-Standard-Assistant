import os, openai, requests, json, time, logging
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

# Load environment variables
load_dotenv()

client = openai.OpenAI()