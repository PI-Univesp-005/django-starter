let scannerReader = null;
let scannerControls = null;
let scannerTargetInput = null;
let scannerLastValue = "";

const scannerModal = document.getElementById("barcodeScannerModal");
const scannerPreview = document.getElementById("barcodeScannerPreview");
const scannerStatus = document.getElementById("barcodeScannerStatus");
const scannerResult = document.getElementById("barcodeScannerResult");
const scannerFormat = document.getElementById("barcodeScannerFormat");

function setScannerStatus(message) {
  if (scannerStatus) {
    scannerStatus.textContent = message;
  }
}

function openScannerModal() {
  if (!scannerModal) return;
  scannerModal.classList.add("is-open");
  scannerModal.setAttribute("aria-hidden", "false");
}

function closeScannerModal() {
  stopScanner();
  if (!scannerModal) return;
  scannerModal.classList.remove("is-open");
  scannerModal.setAttribute("aria-hidden", "true");
}

function stopScanner() {
  if (scannerControls && typeof scannerControls.stop === "function") {
    scannerControls.stop();
  }

  if (scannerReader && typeof scannerReader.reset === "function") {
    scannerReader.reset();
  }

  if (scannerPreview && scannerPreview.srcObject) {
    scannerPreview.srcObject.getTracks().forEach((track) => track.stop());
    scannerPreview.srcObject = null;
  }

  scannerControls = null;
  scannerReader = null;
  setScannerStatus("Desligado");
}

async function buscarProdutoPorCodigo(codigo) {
  if (!codigo) return null;

  try {
    const response = await fetch(`/api/openfoodfacts/?codigo=${encodeURIComponent(codigo)}`);
    const data = await response.json();

    if (!data.ok || !data.encontrado) {
      return null;
    }

    return data;
  } catch (error) {
    console.error("Erro ao buscar produto:", error);
    return null;
  }
}

async function startScanner(targetInputId) {
  try {
    if (!window.ZXing) {
      throw new Error("Biblioteca ZXing não carregou.");
    }

    scannerTargetInput = document.getElementById(targetInputId);

    if (!scannerTargetInput) {
      throw new Error("Campo de código de barras não encontrado.");
    }

    scannerLastValue = "";
    if (scannerResult) scannerResult.textContent = "Nenhum código lido";
    if (scannerFormat) scannerFormat.textContent = "—";

    openScannerModal();
    setScannerStatus("Solicitando permissão da câmera...");

    const hints = new Map();
    hints.set(
      ZXing.DecodeHintType.POSSIBLE_FORMATS,
      [
        ZXing.BarcodeFormat.EAN_13,
        ZXing.BarcodeFormat.EAN_8,
        ZXing.BarcodeFormat.CODE_128,
        ZXing.BarcodeFormat.CODE_39
      ]
    );

    scannerReader = new ZXing.BrowserMultiFormatReader(hints);

    const constraints = {
      audio: false,
      video: {
        facingMode: { ideal: "environment" },
        width: { ideal: 1280 },
        height: { ideal: 720 }
      }
    };

    scannerControls = await scannerReader.decodeFromConstraints(
      constraints,
      scannerPreview,
      async (result, error) => {
        if (result) {
          const text = result.getText();
          const format = result.getBarcodeFormat();

          if (text === scannerLastValue) return;
          scannerLastValue = text;

          if (scannerResult) scannerResult.textContent = text;
          if (scannerFormat) scannerFormat.textContent = format;

          scannerTargetInput.value = text;
          scannerTargetInput.dispatchEvent(new Event("input", { bubbles: true }));
          scannerTargetInput.dispatchEvent(new Event("change", { bubbles: true }));

          setScannerStatus("Buscando produto...");

          const produto = await buscarProdutoPorCodigo(text);

          if (produto && produto.nome) {
            const nomeInput = document.getElementById("nome");
            if (nomeInput && !nomeInput.value.trim()) {
              nomeInput.value = produto.nome;
              nomeInput.dispatchEvent(new Event("input", { bubbles: true }));
              nomeInput.dispatchEvent(new Event("change", { bubbles: true }));
            }
          }

          setScannerStatus("Código lido com sucesso");
          setTimeout(() => {
            closeScannerModal();
          }, 300);
        }
      }
    );

    setScannerStatus("Câmera ativa");
  } catch (error) {
    console.error("Erro ao iniciar scanner:", error);
    setScannerStatus("Erro ao abrir câmera");
    if (scannerResult) {
      scannerResult.textContent = error.message || "Não foi possível acessar a câmera.";
    }
    if (scannerFormat) {
      scannerFormat.textContent = "—";
    }
  }
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && scannerModal && scannerModal.classList.contains("is-open")) {
    closeScannerModal();
  }
});