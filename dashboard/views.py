from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
from io import BytesIO
from django.http import JsonResponse
from datetime import datetime
from .models import TemperatureData, ProductionData

def fetch_external_data():
    url = 'https://www.worldometers.info/pt/' # Adicione o URL do servidor 

    # Enviar uma requisição GET para obter o conteúdo da página
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar o elemento que contém a temperatura
        temperature_element = soup.find('h1')
        
        # Encontrar o elemento que contém o número de produção
        production_element = soup.find('h2')
        
        # Extrair os valores numéricos da temperatura e número de produção
        temperature, production = None, None

        if temperature_element:
            temperature_text = temperature_element.text.split(': ')[1].split(' ')[0]
            try:
                temperature = float(temperature_text)
            except ValueError as e:
                print(f"Error converting temperature to float: {e}")

        if production_element:
            production_text = production_element.text.strip()
            try:
                production = int(production_text)
            except ValueError as e:
                print(f"Error converting production to int: {e}")

        return temperature, production

    return None, None

def save_temperature(request):
    if request.method == 'POST':
        temperature_value = request.POST.get('temperature')
        production_value = request.POST.get('production')

        if temperature_value is not None and production_value is not None:
            # Obtém a data e hora atual
            current_timestamp = datetime.now()

            # Cria uma nova instância de TemperatureData e ProductionData e salva no banco de dados
            TemperatureData.objects.create(
                timestamp=current_timestamp,
                temperature=float(temperature_value),
            )

            ProductionData.objects.create(
                timestamp=current_timestamp,
                production=float(production_value),
            )
            
            return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})

def generate_temperature_chart(timestamps, temperatures):
    fig, ax = plt.subplots()
    ax.plot(timestamps, temperatures, label='Temperatura (°C)')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Temperatura (°C)')
    ax.set_title('Gráfico de Temperatura')
    ax.legend()

    return fig

def get_temperature_history(request):
    # Obtém os últimos 6 registros do banco de dados ordenados por timestamp
    temperature_history = TemperatureData.objects.order_by('-timestamp')[:6]

    # Formata os dados para serem enviados como resposta JSON
    data = {
        'timestamps': [entry.timestamp.strftime('%b') for entry in temperature_history],
        'temperatures': [entry.temperature for entry in temperature_history],
    }

    return JsonResponse(data)

def get_production_history(request):
    # Obtains the latest 6 records from the database ordered by timestamp
    production_history = ProductionData.objects.order_by('-timestamp')[:6]

    # Formats the data to be sent as a JSON response
    data = {
        'timestamps': [entry.timestamp.strftime('%b') for entry in production_history],
        'productions': [entry.production for entry in production_history],
    }

    return JsonResponse(data)

def dashboard(request):
    external_temperature, production = fetch_external_data()
    
    if external_temperature is not None:
        # Aqui você pode salvar a temperatura externa no banco de dados ou utilizá-la conforme necessário
        pass

    # Dados de exemplo para o gráfico Matplotlib
    timestamps = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    temperatures = [25, 30, 22, 35, 28, 33]

    # Criação do gráfico Matplotlib
    fig = generate_temperature_chart(timestamps, temperatures)

    # Salva o gráfico Matplotlib em BytesIO
    image_stream = BytesIO()
    FigureCanvas(fig).print_png(image_stream)
    image_stream.seek(0)

    # Converte a imagem para base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    # Passa a imagem base64 para o template
    context = {
        'temperatura_externa': external_temperature,
        'production': production,
        'graph_html': image_base64,
    }
    return render(request, 'dashboard/dashboard.html', context)

def home(request):
    return render(request, 'dashboard/home.html')
    
def sobre(request):
    return render(request, 'dashboard/sobre.html')
    
def contatos(request):
    return render(request, 'dashboard/contatos.html')