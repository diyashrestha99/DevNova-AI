import joblib


MODEL_PATH = "ml/error_model.pkl"


ERROR_EXPLANATIONS = {
    "NameError":
        "A variable or name is being used before it has been defined.",

    "TypeError":
        "The code appears to be using incompatible data types together.",

    "IndexError":
        "The code is trying to access a list or sequence position that does not exist.",

    "KeyError":
        "The code is trying to access a dictionary key that does not exist.",

    "ValueError":
        "A function received a value that has the wrong format or value.",

    "ZeroDivisionError":
        "The code is attempting to divide a number by zero."
}


ERROR_FIXES = {
    "NameError":
        "Check the variable name and make sure it is defined before use.",

    "TypeError":
        "Check the data types involved and convert them if necessary.",

    "IndexError":
        "Check the index and make sure it is smaller than the list length.",

    "KeyError":
        "Check whether the dictionary contains the requested key.",

    "ValueError":
        "Check the value before converting or processing it.",

    "ZeroDivisionError":
        "Make sure the denominator is not zero before performing division."
}


def predict_error(code):

    model = joblib.load(MODEL_PATH)

    prediction = model.predict([code])[0]

    probabilities = model.predict_proba([code])[0]

    confidence = max(probabilities) * 100

    explanation = ERROR_EXPLANATIONS.get(
        prediction,
        "The model detected a possible programming issue."
    )

    fix = ERROR_FIXES.get(
        prediction,
        "Review the code around the predicted issue."
    )

    return {
        "error_type": prediction,
        "confidence": round(confidence, 2),
        "explanation": explanation,
        "fix": fix
    }