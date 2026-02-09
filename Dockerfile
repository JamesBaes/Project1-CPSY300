FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install pandas matplotlib seaborn
ENV MPLBACKEND=Agg
CMD ["python", "data_analysis.py"]