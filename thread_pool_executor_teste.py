import requests
import concurrent.futures
import hashlib
import time
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re

# Função para obter o status de resposta, calcular o hash SHA256 do conteúdo e contar as palavras de página
def process_url(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        content = response.content
        content_hash = hashlib.sha256(content).hexdigest()

        # Extraindo o texto do HTML
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()

        # Contando as palavras no texto
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)

        return url, status_code, content_hash, word_count
    except requests.RequestException as e:
        return url, None, None, None

# Execução normal (sequencial)
def normal_execution(urls):
    results = []
    for url in urls:
        results.append(process_url(url))
    return results

# Execução com ThreadPoolExecutor (paralelo)
def threadpool_execution(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Mapeia a função process_url para cada URL na lista e executa em paralelo
        results = list(executor.map(process_url, urls))
    return results

# Função para medir o tempo de execução para diferentes números de URLs
def measure_execution_time(urls_list, execution_function):
    num_urls = []
    execution_times = []

    for urls in urls_list:
        start_time = time.time()
        execution_function(urls)
        end_time = time.time()

        num_urls.append(len(urls))
        execution_times.append(end_time - start_time)

    return num_urls, execution_times


if __name__ == "__main__":
    urls = [
        "https://www.google.com",
        "https://www.youtube.com",
        "https://www.instagram.com",
        "https://www.facebook.com",
        "https://www.linkedin.com",
        "https://www.wikipedia.com",
        "https://www.globo.com",
        "https://www.notion.so",
        "https://www.gmail.com",
        "https://www.github.com",
        "https://www.hotmail.com",
        "https://www.netflix.com"
    ]

    num_urls = []
    normal_execution_times = []
    threadpool_execution_times = []

    for i in range(1, len(urls) + 1):
        subset_urls = urls[:i]

        print("Execução Normal:")
        _, normal_time = measure_execution_time([subset_urls], normal_execution)
        normal_execution_times.append(normal_time[0])
        print(f"Tempo de execução (normal): {normal_time[0]:.2f} segundos")

        print("\nThreadPoolExecutor:")
        _, threadpool_time = measure_execution_time([subset_urls], threadpool_execution)
        threadpool_execution_times.append(threadpool_time[0])
        print(f"Tempo de execução (ThreadPoolExecutor): {threadpool_time[0]:.2f} segundos")

        num_urls.append(i)

    plt.figure(figsize=(10,6))
    plt.plot(num_urls, normal_execution_times, label='Execução convencional', color='blue')
    plt.plot(num_urls, threadpool_execution_times, label='Execução com ThreadPoolExecutor', color='orange')
    plt.xlabel('Número de URLs')
    plt.ylabel('Tempo de execução (s)')
    plt.title('Diferença no tempo de execução com o aumento da complexidade da tarefa')
    
    # Adicionando marcador e rótulo
    for i in num_urls:
            if i % 3 == 0 and i != 6:
                plt.scatter(num_urls[i-1], normal_execution_times[i-1], color='blue')
                plt.annotate(f'{normal_execution_times[i-1]:.2f}', (num_urls[i-1], normal_execution_times[i-1]), 
                             textcoords="offset points", xytext=(0,10), ha='center', fontsize=12)
    
                plt.scatter(num_urls[i-1], threadpool_execution_times[i-1], color='orange')
                plt.annotate(f'{threadpool_execution_times[i-1]:.2f}', (num_urls[i-1], threadpool_execution_times[i-1]), 
                             textcoords="offset points", xytext=(0,10), ha='center', fontsize=12)
                
    plt.xticks(num_urls)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.legend()
    plt.show()
