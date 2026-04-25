from models.vector_store import VectorStore
from services.storage_service import S3StorageService
from services.llm_service import LLMService
from config import Config
import os
from langchain_classic.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
import logging
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


vector_store = VectorStore(collection_name="my_collection")
StorageService = S3StorageService()
LLMService = LLMService(vector_store)


@app.route("/")
def index():
    return render_template("index.html")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_document(file):
    """Process the uploaded document and return chunks and temp path."""
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)

    try:
        file.save(temp_path)

        if file.filename.endswith(".pdf"):
            loader = PyPDFLoader(temp_path)
            documents = loader.load()
        elif file.filename.endswith(".txt"):
            loader = TextLoader(temp_path)
            documents = loader.load()
        else:
            raise ValueError("Unsupported file type.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)

        return chunks, temp_path, temp_dir

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        os.rmdir(temp_dir)
        raise


@app.route("/upload", methods=["POST"])
def upload_documents():
    try:
        logger.debug("Received file upload request.")

        if "file" not in request.files:
            logger.warning("No file part in the request.")
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            logger.warning("No file selected for uploading.")
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith((".pdf", ".txt")):
            logger.warning("Unsupported file type uploaded.")
            return jsonify(
                {"error": "Unsupported file type. Please upload a PDF or TXT file."}
            ), 400

        try:
            chunks, temp_path, temp_dir = process_document(file)
            logger.debug(f"Document processed into {len(chunks)} chunks.")
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return jsonify({"error": "Error processing document."}), 500

        try:
            upload_success = StorageService.upload_file(temp_path, file.filename)
            logger.debug(
                f"File upload to S3 {'succeeded' if upload_success else 'failed'}."
            )
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            return jsonify({"error": "Error uploading file to storage."}), 500

        try:
            vector_store.add_documents(documents=chunks)
            logger.debug("Chunks added to vector store successfully.")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            return jsonify({"error": "Error adding documents to vector store."}), 500

        if os.path.exists(temp_path):
            os.remove(temp_path)
        os.rmdir(temp_dir)

        return jsonify({"message": "File uploaded and processed successfully."}), 200

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500


@app.route("/query", methods=["POST"])
def query():
    data = request.json
    if "question" not in data:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = LLMService.get_response(data["question"])
        return jsonify({"response": response}), 200
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({"error": "Error processing query."}), 500


@app.route("/plot")
def plot():
    return render_template("plot.html")


@app.route("/api/plot-data", methods=["POST"])
def get_plot_data():
    try:
        data = request.json
        chart_type = data.get("chartType", "line")
        x_data = data.get("xData", [])
        y_data = data.get("yData", [])
        title = data.get("title", "Chart")

        import base64
        import io
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots(figsize=(10, 6), facecolor="#0a0e17")
        ax.set_facecolor("#0a0e17")

        colors = ["#6366f1", "#a855f7", "#ec4899", "#10b981", "#f59e0b"]

        if chart_type == "line":
            ax.plot(
                x_data, y_data, color=colors[0], linewidth=2, marker="o", markersize=6
            )
        elif chart_type == "bar":
            ax.bar(x_data, y_data, color=colors[0], edgecolor="#334155")
        elif chart_type == "scatter":
            ax.scatter(x_data, y_data, c=colors[0], s=100, alpha=0.7)
        elif chart_type == "area":
            ax.fill_between(x_data, y_data, color=colors[0], alpha=0.3)
            ax.plot(x_data, y_data, color=colors[0], linewidth=2)
        elif chart_type == "pie":
            ax.pie(
                y_data, labels=x_data, colors=colors[: len(y_data)], autopct="%1.1f%%"
            )

        ax.set_title(title, color="#f1f5f9", fontsize=14, fontweight="bold", pad=20)
        ax.tick_params(colors="#7c8db5")

        for spine in ax.spines.values():
            spine.set_color("#2a3548")

        if chart_type != "pie":
            ax.set_xlabel("X", color="#7c8db5", fontsize=12)
            ax.set_ylabel("Y", color="#7c8db5", fontsize=12)

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, facecolor="#0a0e17")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close()

        return jsonify({"image": f"data:image/png;base64,{img_base64}"}), 200

    except Exception as e:
        logger.error(f"Error generating plot: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
