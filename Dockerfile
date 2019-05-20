FROM gorialis/discord.py:minimal

WORKDIR .

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "christopher.py"]