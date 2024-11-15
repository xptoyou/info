from flask import Flask, request, jsonify, send_file
from xp_interpreter import XPInterpreter
import os

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_xp():
    data = request.get_json()
    code = data.get('code', '')

    interpreter = XPInterpreter()
    output = []

    # Override print to capture interpreter output
    def capture_print(*args):
        output.append(' '.join(map(str, args)))

    interpreter.print = capture_print  # Replace print in XP interpreter
    interpreter.execute(code)

    return jsonify({'output': '\n'.join(output)})

@app.route('/download', methods=['GET'])
def download_xp_file():
    # Create a sample XP file
    file_content = """var x = 10
var y = 20
if x + y > 25 {
    print("Sum is greater than 25")
} else {
    print("Sum is 25 or less")
}"""
    file_path = "xptoyou.xp"
    
    # Write the file content
    with open(file_path, "w") as file:
        file.write(file_content)

    # Serve the file as a download
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
