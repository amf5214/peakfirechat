from flask import Flask, render_template, request, redirect, url_for, json, Response, jsonify, make_response, flash
import logging

from src.models import *
from src.authentication import *
from src.image_handling import *

class AdminPageRendering():
