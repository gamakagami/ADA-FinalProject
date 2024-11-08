import os
from deepface import DeepFace
import cv2

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress all TensorFlow logs except errors

# Exercises data based on intensity and emotion
exercises = {
    "angry": {"low": "Medicine ball slam", "medium": "Boxing", "high": "Heavy Lifting"},
    "disgust": {"low": "Twist", "medium": "Pulldown", "high": "Squats"},
    "fear": {"low": "Treadmill", "medium": "Elliptical", "high": "Burpees"},
    "neutral": {"low": "Leg press", "medium": "Rowing", "high": "Barbells"},
    "sad": {"low": "Walking", "medium": "Jogging", "high": "Running"},
    "happy": {"low": "Brisk Walking", "medium": "Yoga", "high": "Pilates"},
    "surprise": {"low": "Stretches", "medium": "Zumba", "high": "Jump training"}
}

def detect_emotion(image_path):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"File '{image_path}' does not exist. Please check the path.")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image '{image_path}' could not be loaded. Ensure it's a valid image file.")
    else:
        print("Image loaded successfully!")  # Debug output to confirm loading

    # Analyze emotion and returns a dictionary of emotions and scores
    emotion_analysis = DeepFace.analyze(image, actions=['emotion'])[0]
    sorted_emotions = sorted(emotion_analysis['emotion'].items(), key=lambda x: x[1], reverse=True)
    return [emotion for emotion, _ in sorted_emotions]  # Return list of sorted emotions

def create_sorted_exercise_list(emotion_priority_list, ideal_intensity):
    sorted_exercise_list = []
    for emotion in emotion_priority_list:
        if emotion not in exercises:
            continue

        # Add exercises based on intensity preference first
        if ideal_intensity in exercises[emotion]:
            sorted_exercise_list.append(exercises[emotion][ideal_intensity])

        # Add remaining exercises (other intensities) for this emotion
        for intensity in ['low', 'medium', 'high']:
            if intensity != ideal_intensity and intensity in exercises[emotion]:
                sorted_exercise_list.append(exercises[emotion][intensity])

    return sorted_exercise_list

def get_user_preferences():
    while True:
        try:
            ideal_time = int(input("Enter ideal time for exercise (minutes): "))
            if ideal_time <= 0:
                print("Please enter a positive number for time.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number for time.")
            continue

        ideal_intensity = input("Enter ideal intensity (low, medium, high): ").lower()
        if ideal_intensity not in ['low', 'medium', 'high']:
            print("Invalid intensity. Please enter 'low', 'medium', or 'high'.")
            continue

        return ideal_time, ideal_intensity

def exercise_program(image_path):
    performed_exercises = []

    try:
        emotion_priority_list = detect_emotion(image_path)
        print(f"Detected Emotions in order of dominance: {emotion_priority_list}")

        ideal_time, ideal_intensity = get_user_preferences()
        sorted_exercise_list = create_sorted_exercise_list(emotion_priority_list, ideal_intensity)
        print(f"Sorted Exercise List (Most to Least Compatible): {sorted_exercise_list}")

        cumulative_exercise_list = []
        current_index = 0

        while current_index < len(sorted_exercise_list):
            suggested_exercise = sorted_exercise_list[current_index]

            if suggested_exercise in performed_exercises:
                current_index += 1
                continue

            if suggested_exercise not in cumulative_exercise_list:
                cumulative_exercise_list.append(suggested_exercise)
                print(f"Added to cumulative list: {suggested_exercise}")
                print(f"Current Cumulative Exercise List: {cumulative_exercise_list}")

            print(f"Suggested Exercise: {suggested_exercise}")

            user_accept = input("Do you accept this exercise? (yes/no): ").lower()
            if user_accept not in ["yes", "no"]:
                print("Invalid response. Please enter 'yes' or 'no'.")
                continue

            if user_accept == "yes":
                print(f"Performing Exercise: {suggested_exercise}")
                performed_exercises.append(suggested_exercise)

                continue_exercising = input("Do you want to continue with another exercise? (yes/no): ").lower()
                if continue_exercising not in ["yes", "no"]:
                    print("Invalid response. Please enter 'yes' or 'no'.")
                    continue

                if continue_exercising == "no":
                    print(f"Final Cumulative Exercise List: {cumulative_exercise_list}")
                    print(f"Performed Exercises: {performed_exercises}")
                    return

                sorted_exercise_list = create_new_compatible_list(suggested_exercise)
                current_index = 0
                continue
            else:
                current_index += 1
                print("Suggesting the next exercise based on the sorted list.")

        print("No more exercises available.")
        print(f"Final Cumulative Exercise List: {cumulative_exercise_list}")
        print(f"Performed Exercises: {performed_exercises}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

def create_new_compatible_list(previous_exercise):
    intensity_order = {'low': 0, 'medium': 1, 'high': 2}
    exercises_with_intensity = [
        (exercise, intensity)
        for emotion, intensity_map in exercises.items()
        for intensity, exercise in intensity_map.items()
        if exercise != previous_exercise
    ]
    exercises_with_intensity.sort(key=lambda x: intensity_order[x[1]])
    sorted_exercise_list = [exercise for exercise, _ in exercises_with_intensity]

    print(f"Created new list of compatible exercises based on {previous_exercise}: {sorted_exercise_list}")
    return sorted_exercise_list

def suggest_exercise(emotion, intensity):
    return exercises[emotion][intensity] if emotion in exercises and intensity in exercises[emotion] else None

exercise_program("gam.png")  # Ensure this path is correct or update it accordingly
