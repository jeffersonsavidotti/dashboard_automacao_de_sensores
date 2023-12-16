from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
from io import BytesIO
from django.http import JsonResponse
from .models import TemperatureData



def fetch_external_temperature():
    url = 'http://192.168.239.33' #Adicione o url do site com as informações http://192.168.239.33

    # Enviar uma requisição GET para obter o conteúdo da página
    response = requests.get(url)

    # Imprimir o conteúdo da resposta para análise
    print(response.text)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ajuste da classe para encontrar o elemento correto no HTML
        temperature_element = soup.find('') # h1

        if temperature_element:
            # Extrair apenas o valor numérico da temperatura
            temperature_text = temperature_element.text.split(': ')[1].split(' ')[0]
            
            # Tentar converter o valor para float
            try:
                temperature_float = float(temperature_text)
                return temperature_float
            except ValueError as e:
                print(f"Error converting temperature to float: {e}")

    return None

def save_temperature(request):
    if request.method == 'POST':
        temperature_value = request.POST.get('temperature')
        if temperature_value is not None:
            TemperatureData.objects.create(temperature=float(temperature_value))
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

def dashboard(request):
    external_temperature = fetch_external_temperature()
    
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
        'graph_html': image_base64,
    }

    return render(request, 'dashboard/dashboard.html', context)
