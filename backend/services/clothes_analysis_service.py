from PIL import Image
import torch

# Try to import the OpenAI CLIP package. If another package named `clip`
# is installed or a local module shadows it, the expected `load` function
# may be missing which produces the AttributeError you saw.
try:
    import clip as _clip
except Exception:
    _clip = None

device = "cuda" if torch.cuda.is_available() else "cpu"

# lazy-loaded model + preprocess to avoid import-time failures
_clip_model = None
_preprocess = None

categories = ["t-shirt", "jacket", "dress", "pants", "skirt"]

def _get_clip_model():
    """Return (model, preprocess). Raise a helpful error if CLIP isn't available.

    This delays loading until the function is called so the module can be imported
    even when CLIP isn't installed, and provides a clear message on how to fix it.
    """
    global _clip_model, _preprocess, _clip

    if _clip is None:
        raise RuntimeError(
            "The OpenAI CLIP package is not available or a different 'clip' package is installed.\n"
            "Install the official CLIP with: pip install git+https://github.com/openai/CLIP.git"
        )

    if _clip_model is None or _preprocess is None:
        # clip.load may raise its own errors (e.g., missing torch). Let those bubble up.
        _clip_model, _preprocess = _clip.load("ViT-B/32", device=device)

    return _clip_model, _preprocess


def analyze_clothes(image_path):
    model, preprocess = _get_clip_model()

    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

    text = _clip.tokenize(categories).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

        similarity = (image_features @ text_features.T).softmax(dim=-1)

    probs = similarity.cpu().numpy()[0]

    idx = probs.argmax()

    return {
        "category": categories[idx],
        "confidence": float(probs[idx])
    }