
import os
import sys
import shutil
import subprocess
import yaml

from signLanguage.utils.main_utils import read_yaml_file
from signLanguage.logger import logging
from signLanguage.exception import SignException

from signLanguage.entity.config_entity import ModelTrainerConfig
from signLanguage.entity.artifacts_entity import ModelTrainerArtifact


class ModelTrainer:

    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig
    ):

        try:

            self.model_trainer_config = (
                model_trainer_config
            )

            logging.info(
                "ModelTrainer initialized successfully."
            )

        except Exception as e:

            raise SignException(
                e,
                sys
            ) from e

    # ============================================================
    # INITIATE MODEL TRAINER
    # ============================================================

    def initiate_model_trainer(
        self
    ) -> ModelTrainerArtifact:

        logging.info(
            "================================================"
        )

        logging.info(
            "Entered initiate_model_trainer method."
        )

        try:

            # ====================================================
            # PROJECT ROOT
            # ====================================================

            project_root = os.getcwd()

            logging.info(
                f"Project root: {project_root}"
            )

            # ====================================================
            # ARTIFACTS PATH
            # ====================================================

            artifacts_path = os.path.join(
                project_root,
                "artifacts"
            )

            if not os.path.exists(
                artifacts_path
            ):

                raise FileNotFoundError(
                    f"Artifacts directory not found at: "
                    f"{artifacts_path}"
                )

            logging.info(
                f"Artifacts path: {artifacts_path}"
            )

            # ====================================================
            # FIND DATA.YAML
            # ====================================================

            logging.info(
                "Searching for data.yaml..."
            )

            data_yaml_candidates = []

            for root, dirs, files in os.walk(
                artifacts_path
            ):

                if "data.yaml" in files:

                    data_yaml_path_candidate = os.path.join(
                        root,
                        "data.yaml"
                    )

                    data_yaml_candidates.append(
                        data_yaml_path_candidate
                    )

                    logging.info(
                        f"Found data.yaml: "
                        f"{data_yaml_path_candidate}"
                    )

            # ====================================================
            # CHECK DATA.YAML
            # ====================================================

            if not data_yaml_candidates:

                raise FileNotFoundError(
                    f"data.yaml not found inside: "
                    f"{artifacts_path}"
                )

            # ====================================================
            # SELECT LATEST DATA.YAML
            # ====================================================

            data_yaml_path = max(
                data_yaml_candidates,
                key=os.path.getmtime
            )

            logging.info(
                f"Selected data.yaml: "
                f"{data_yaml_path}"
            )

            # ====================================================
            # FEATURE STORE PATH
            # ====================================================

            feature_store_path = os.path.dirname(
                data_yaml_path
            )

            logging.info(
                f"Feature store path: "
                f"{feature_store_path}"
            )

            if not os.path.exists(
                feature_store_path
            ):

                raise FileNotFoundError(
                    f"Feature store not found at: "
                    f"{feature_store_path}"
                )

            # ====================================================
            # TRAIN IMAGE PATH
            # ====================================================

            train_path = os.path.join(
                feature_store_path,
                "train",
                "images"
            )

            logging.info(
                f"Train images path: {train_path}"
            )

            if not os.path.exists(
                train_path
            ):

                raise FileNotFoundError(
                    f"Train images path not found: "
                    f"{train_path}"
                )

            # ====================================================
            # TRAIN LABEL PATH
            # ====================================================

            train_label_path = os.path.join(
                feature_store_path,
                "train",
                "labels"
            )

            logging.info(
                f"Train labels path: "
                f"{train_label_path}"
            )

            if not os.path.exists(
                train_label_path
            ):

                raise FileNotFoundError(
                    f"Train labels path not found: "
                    f"{train_label_path}"
                )

            # ====================================================
            # VALID IMAGE PATH
            # ====================================================

            valid_path = os.path.join(
                feature_store_path,
                "valid",
                "images"
            )

            logging.info(
                f"Validation images path: {valid_path}"
            )

            if not os.path.exists(
                valid_path
            ):

                raise FileNotFoundError(
                    f"Validation images path not found: "
                    f"{valid_path}"
                )

            # ====================================================
            # VALID LABEL PATH
            # ====================================================

            valid_label_path = os.path.join(
                feature_store_path,
                "valid",
                "labels"
            )

            logging.info(
                f"Validation labels path: "
                f"{valid_label_path}"
            )

            if not os.path.exists(
                valid_label_path
            ):

                raise FileNotFoundError(
                    f"Validation labels path not found: "
                    f"{valid_label_path}"
                )

            # ====================================================
            # READ DATA.YAML
            # ====================================================

            logging.info(
                "Reading data.yaml..."
            )

            with open(
                data_yaml_path,
                "r"
            ) as stream:

                data_config = yaml.safe_load(
                    stream
                )

            if data_config is None:

                raise ValueError(
                    "data.yaml is empty."
                )

            # ====================================================
            # NUMBER OF CLASSES
            # ====================================================

            if "nc" not in data_config:

                raise KeyError(
                    "nc is missing from data.yaml"
                )

            num_classes = int(
                data_config["nc"]
            )

            logging.info(
                f"Number of classes: {num_classes}"
            )

            # ====================================================
            # CLASS NAMES
            # ====================================================

            if "names" not in data_config:

                raise KeyError(
                    "names is missing from data.yaml"
                )

            logging.info(
                f"Class names: "
                f"{data_config['names']}"
            )

            # ====================================================
            # UPDATE TRAIN AND VALID PATH
            # ====================================================

            data_config["train"] = os.path.abspath(
                train_path
            )

            data_config["val"] = os.path.abspath(
                valid_path
            )

            # ====================================================
            # CREATE UPDATED DATA.YAML
            # ====================================================

            updated_data_yaml_path = os.path.join(
                feature_store_path,
                "updated_data.yaml"
            )

            with open(
                updated_data_yaml_path,
                "w"
            ) as file:

                yaml.dump(
                    data_config,
                    file,
                    default_flow_style=False
                )

            logging.info(
                f"Updated data.yaml saved at: "
                f"{updated_data_yaml_path}"
            )

            logging.info(
                f"Train path: "
                f"{data_config['train']}"
            )

            logging.info(
                f"Validation path: "
                f"{data_config['val']}"
            )

            # ====================================================
            # YOLOV5 DIRECTORY
            # ====================================================

            yolov5_path = os.path.join(
                project_root,
                "yolov5"
            )

            if not os.path.exists(
                yolov5_path
            ):

                raise FileNotFoundError(
                    f"YOLOv5 directory not found at: "
                    f"{yolov5_path}"
                )

            logging.info(
                f"YOLOv5 directory found: "
                f"{yolov5_path}"
            )

            # ====================================================
            # MODEL WEIGHT
            # ====================================================

            weight_name = (
                self.model_trainer_config.weight_name
            )

            logging.info(
                f"Model weight: {weight_name}"
            )

            # ====================================================
            # MODEL CONFIG FILE NAME
            # ====================================================

            model_config_file_name = os.path.splitext(
                os.path.basename(
                    weight_name
                )
            )[0]

            model_config_path = os.path.join(
                yolov5_path,
                "models",
                f"{model_config_file_name}.yaml"
            )

            if not os.path.exists(
                model_config_path
            ):

                raise FileNotFoundError(
                    f"Model config not found at: "
                    f"{model_config_path}"
                )

            logging.info(
                f"Model config found: "
                f"{model_config_path}"
            )

            # ====================================================
            # READ MODEL CONFIG
            # ====================================================

            config = read_yaml_file(
                model_config_path
            )

            if config is None:

                raise ValueError(
                    "YOLOv5 model configuration is empty."
                )

            # ====================================================
            # UPDATE NUMBER OF CLASSES
            # ====================================================

            config["nc"] = num_classes

            # ====================================================
            # CREATE CUSTOM MODEL CONFIG
            # ====================================================

            custom_model_config_path = os.path.join(
                yolov5_path,
                "models",
                f"custom_{model_config_file_name}.yaml"
            )

            with open(
                custom_model_config_path,
                "w"
            ) as file:

                yaml.dump(
                    config,
                    file,
                    default_flow_style=False
                )

            logging.info(
                f"Custom model config created: "
                f"{custom_model_config_path}"
            )

            # ====================================================
            # CHECK TRAIN.PY
            # ====================================================

            train_script = os.path.join(
                yolov5_path,
                "train.py"
            )

            if not os.path.exists(
                train_script
            ):

                raise FileNotFoundError(
                    f"train.py not found at: "
                    f"{train_script}"
                )

            logging.info(
                f"train.py found: {train_script}"
            )

            # ====================================================
            # TRAINING PARAMETERS
            # ====================================================

            batch_size = int(
                self.model_trainer_config.batch_size
            )

            no_epochs = int(
                self.model_trainer_config.no_epoch
            )

            logging.info(
                f"Batch size: {batch_size}"
            )

            logging.info(
                f"Epochs: {no_epochs}"
            )

            # ====================================================
            # TRAINING COMMAND
            # ====================================================

            command = [

                sys.executable,

                "train.py",

                "--img",
                "416",

                "--batch",
                str(batch_size),

                "--epochs",
                str(no_epochs),

                "--data",
                os.path.abspath(
                    updated_data_yaml_path
                ),

                "--cfg",
                os.path.join(
                    "models",
                    f"custom_{model_config_file_name}.yaml"
                ),

                "--weights",
                weight_name,

                "--name",
                "yolov5s_results",

                "--cache"
            ]

            logging.info(
                "Starting YOLOv5 model training..."
            )

            logging.info(
                "Training command:"
            )

            logging.info(
                " ".join(command)
            )

            # ====================================================
            # RUN YOLOV5 TRAINING
            # ====================================================

            result = subprocess.run(
                command,
                cwd=yolov5_path,
                check=False
            )

            # ====================================================
            # CHECK TRAINING RESULT
            # ====================================================

            if result.returncode != 0:

                raise RuntimeError(
                    f"YOLOv5 model training failed "
                    f"with return code: "
                    f"{result.returncode}"
                )

            logging.info(
                "YOLOv5 training completed successfully."
            )

            # ====================================================
            # YOLOV5 TRAINING RESULTS PATH
            # ====================================================

            runs_dir = os.path.join(
                yolov5_path,
                "runs",
                "train"
            )

            logging.info(
                f"Searching training results in: "
                f"{runs_dir}"
            )

            if not os.path.exists(
                runs_dir
            ):

                raise FileNotFoundError(
                    f"YOLOv5 training runs directory "
                    f"not found: {runs_dir}"
                )

            # ====================================================
            # FIND ALL YOLOV5 RESULT DIRECTORIES
            # ====================================================

            run_dirs = []

            for folder in os.listdir(
                runs_dir
            ):

                folder_path = os.path.join(
                    runs_dir,
                    folder
                )

                if (
                    os.path.isdir(folder_path)
                    and
                    folder.startswith(
                        "yolov5s_results"
                    )
                ):

                    run_dirs.append(
                        folder_path
                    )

            if not run_dirs:

                raise FileNotFoundError(
                    f"No YOLOv5 training result found "
                    f"in: {runs_dir}"
                )

            logging.info(
                f"Found training directories: "
                f"{run_dirs}"
            )

            # ====================================================
            # FIND BEST.PT
            # ====================================================

            best_model_candidates = []

            for run_dir in run_dirs:

                candidate = os.path.join(
                    run_dir,
                    "weights",
                    "best.pt"
                )

                logging.info(
                    f"Checking model path: "
                    f"{candidate}"
                )

                if os.path.isfile(
                    candidate
                ):

                    best_model_candidates.append(
                        candidate
                    )

                    logging.info(
                        f"Found best.pt: "
                        f"{candidate}"
                    )

            # ====================================================
            # CHECK BEST.PT
            # ====================================================

            if not best_model_candidates:

                raise FileNotFoundError(
                    f"best.pt was not found in any "
                    f"YOLOv5 training run: {runs_dir}"
                )

            # ====================================================
            # SELECT LATEST BEST.PT
            # ====================================================

            best_model_path = max(
                best_model_candidates,
                key=os.path.getmtime
            )

            logging.info(
                f"Best model selected: "
                f"{best_model_path}"
            )

            # ====================================================
            # COPY BEST MODEL TO YOLOV5 ROOT
            # ====================================================

            yolov5_model_path = os.path.join(
                yolov5_path,
                "best.pt"
            )

            shutil.copy2(
                best_model_path,
                yolov5_model_path
            )

            logging.info(
                f"Model copied to: "
                f"{yolov5_model_path}"
            )

            # ====================================================
            # CREATE MODEL TRAINER DIRECTORY
            # ====================================================

            os.makedirs(
                self.model_trainer_config.model_trainer_dir,
                exist_ok=True
            )

            # ====================================================
            # FINAL MODEL PATH
            # ====================================================

            final_model_path = os.path.join(
                self.model_trainer_config.model_trainer_dir,
                "best.pt"
            )

            shutil.copy2(
                best_model_path,
                final_model_path
            )

            logging.info(
                f"Final model saved at: "
                f"{final_model_path}"
            )

            # ====================================================
            # CREATE MODEL TRAINER ARTIFACT
            # ====================================================

            model_trainer_artifact = (
                ModelTrainerArtifact(
                    trained_model_file_path=final_model_path
                )
            )

            logging.info(
                "ModelTrainer completed successfully."
            )

            logging.info(
                "================================================"
            )

            return model_trainer_artifact

        except Exception as e:

            logging.error(
                f"Model training failed: {e}"
            )

            raise SignException(
                e,
                sys
            ) from e
