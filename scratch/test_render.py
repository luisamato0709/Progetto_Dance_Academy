from app import app
import sys

with app.test_request_context():
    try:
        print("Rendering index...")
        response = app.view_functions['index']()
        # Se è un oggetto response di Flask (che render_template restituisce)
        if hasattr(response, 'data'):
            html = response.data.decode('utf-8')
        else:
            html = response # Nel caso fosse già una stringa
        print("Index rendered successfully!")
        print(f"HTML Length: {len(html)}")
        # print(html[:500])
    except Exception as e:
        print(f"Error rendering index: {e}")
        import traceback
        traceback.print_exc()
