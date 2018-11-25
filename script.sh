#!/bin/bash

source env/bin/activate
flake8 .
pylint 2048-game/ wechat_analyse/ climb-zhihu/ image-to-str/ 
