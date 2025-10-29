import os 
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

load_dotenv()

class ScrappingService:
    def __init__(self):
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        self.api_url = os.getenv("FIRECRAWL_API_URL")

        self.app = FirecrawlApp(api_key=self.api_key, api_url=self.api_url)

    def scrape_website(self, url, collection_name, max_links=20):
        try:
            # Mapeia o site para encontrar todos os links
            print(f"Mapping website: {url}")
            map_result = self.app.map(url)

            # Extrai os links do resultado
            links = []
            if hasattr(map_result, 'links'):
                links = map_result.links
            elif isinstance(map_result, dict) and 'links' in map_result:
                links = map_result['links']
            
            # Debug: verifica o tipo de links
            print(f"Type of links: {type(links)}")
            print(f"First link type: {type(links[0]) if links else 'No links'}")

            if not links:
                raise Exception("No links found to scrape.")

            links = links[:max_links]

            print(f"Found {len(links)} links to scrape.")

            # Cria o diretório da coleção
            collection_path = f"data/collections/{collection_name}"
            os.makedirs(collection_path, exist_ok=True)

            saved_count = 0
            
            # Itera sobre cada link e faz o scraping
            for i, link_item in enumerate(links):
                try:
                    # Extrai a URL do objeto LinkResult de múltiplas formas
                    link_url = None

                    # 🔹 Se o item for uma lista (ex: [LinkResult(...)]), pega o primeiro elemento
                    if isinstance(link_item, list) and len(link_item) > 0:
                        link_item = link_item[0]

                    # 🔹 Agora trata os diferentes formatos possíveis
                    if isinstance(link_item, str):
                        link_url = link_item
                    elif hasattr(link_item, "url"):
                        link_url = link_item.url
                    elif isinstance(link_item, dict):
                        link_url = link_item.get("url")

                    # 🔹 Verifica se é realmente uma string
                    if not isinstance(link_url, str):
                        print(f"⚠️ Invalid link (not string): {link_item}")
                        continue
                    
                    if not link_url:
                        print(f"Could not extract URL from link {i+1}: {link_item}")
                        continue

                    print(f"Scraping {i+1}/{len(links)}: {link_url}")

                    # Faz o scraping da página individual - passando STRING
                    scrape_result = self.app.scrape(url=str(link_url))
                    
                    # Extrai o conteúdo markdown
                    markdown_content = None
                    if hasattr(scrape_result, 'markdown'):
                        markdown_content = scrape_result.markdown
                    elif hasattr(scrape_result, 'data'):
                        if hasattr(scrape_result.data, 'markdown'):
                            markdown_content = scrape_result.data.markdown
                        elif isinstance(scrape_result.data, dict):
                            markdown_content = scrape_result.data.get('markdown')
                    elif isinstance(scrape_result, dict):
                        data = scrape_result.get('data', {})
                        if isinstance(data, dict):
                            markdown_content = data.get('markdown')
                        else:
                            markdown_content = scrape_result.get('markdown')
                    
                    if markdown_content:
                        # Salva o arquivo markdown
                        filename = f"{collection_path}/{i+1}.md"
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(markdown_content)
                        saved_count += 1
                        print(f"✓ Saved: {filename}")
                    else:
                        print(f"✗ No markdown content found for {link_url}")
                        
                except Exception as link_error:
                    print(f"✗ Error scraping link {i}: {link_error}")
                    continue
            
            print(f"\nScraping completed: {saved_count}/{len(links)} pages saved")
            return {"success": True, "files": saved_count, "total_links": len(links)}

        except Exception as e:
            print(f"Error during scraping: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}