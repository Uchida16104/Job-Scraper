FROM mcr.microsoft.com/dotnet/sdk:latest AS csharp-build

WORKDIR /csharp
COPY csharp/ ./
RUN dotnet restore JobScraperCore.csproj
RUN dotnet publish JobScraperCore.csproj -c Release -o /app/csharp

FROM python:latest

RUN apt-get update && apt-get install -y \
    wget \
    apt-transport-https \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb

RUN apt-get update && apt-get install -y \
    dotnet-runtime-8.0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=csharp-build /app/csharp /app/csharp
COPY python/ /app/python/
COPY requirements.txt /app/
COPY data/ /app/data/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
ENV PATH="/app/csharp:${PATH}"

WORKDIR /app/python

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
