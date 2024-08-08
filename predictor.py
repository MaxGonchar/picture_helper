from img_data_transformer import prepare_tags_for_prediction
import dao


def predict_likelihood_of_image(tags: list[str]) -> tuple[bool, float]:
    prediction_data = prepare_tags_for_prediction(tags)
    predictor = dao.get_predictor()
    is_good = bool(predictor.predict([prediction_data])[0])
    likelihood = int((predictor.predict_proba([prediction_data])[0][1]) * 100)
    return is_good, likelihood
