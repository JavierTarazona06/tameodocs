# Innovation Prize Preparation Brief

## Working Innovation Title

**A data-centric simulation-to-real pipeline for autonomous buoy detection in the MEBC AI Class.**

This document is a factual base for preparing the Innovation Prize video, script, and slides. It is not a final script. It uses claims supported by the repository documents, the MEBC Innovation Prize guideline PDF, and the adjacent BlueBoat autonomous-mode code workspace.

## Prize Context

According to `InnovationVideo/MEBC2026 - TechTalk Prizes (1) (1).pdf`, the Innovation Prize submission includes:

- a pitch video of maximum 2 minutes;
- technical documentation for evaluation;
- assessment on novelty, problem solving and value creation, market potential, feasibility, scalability, and proof of concept.

The innovation should therefore be presented as both technically credible and practically useful for the future of autonomous maritime systems.

## Core Message

Our innovation is not only an autonomous boat component. It is a **data-centric simulation-to-real validation pipeline** that links:

1. a real robotic test platform, the BlueBoat, used before the final MEBC competition boat is available;
2. a maritime perception dataset and augmentation process designed to make buoy detection robust to real sea conditions;
3. a BlueBoat-adapted DWA local planner that evaluates feasible short-horizon boat motions instead of only following static waypoints;
4. an embedded integration path toward Jetson, ZED cameras, BlueOS, ArduPilot, MAVLink, QGroundControl, and the final boat architecture.

The goal is to reduce the gap between offline AI development and real autonomous navigation at the Monaco Energy Boat Challenge.

## Problem Addressed

The project faced two major constraints documented in the repository:

- the final competition chassis was available late, which could have blocked software, perception, and control development;
- the initial number of clean buoy and docking images was limited, which made it difficult to train a robust perception model for maritime scenes.

In a maritime competition, these constraints are important because real water tests are expensive in time, logistics, safety preparation, and weather dependency. A system that can be tested earlier and trained on more realistic visual conditions creates direct value for the team.

## Innovation Pillar 1: BlueBoat as a Validation Platform

The BlueBoat was used as a real test bench before full integration on the final competition boat. The verified role of the BlueBoat in the repo is:

- keeping software development active despite late access to the final chassis;
- validating system architecture choices, communications, and first autonomous system components;
- integrating the Jetson, cameras, and embedded network;
- supporting the AI integration before transition to the final boat;
- testing MAVLink communication, BlueOS access, QGroundControl supervision, and remote access to the Jetson;
- preparing the transition toward the real boat by integrating selected sensors and action-oriented test benches.

This creates an innovation value: the team can validate perception integration, communication, control interfaces, and decision-chain assumptions before using the real competition boat.

Important wording for the video:

- Say: **"BlueBoat reduces dependency on the final chassis and lowers unnecessary risk during early validation."**
- Say: **"It allows repeatable bench and platform tests before full-scale trials."**
- Avoid saying: **"We measured a specific testing cost reduction."** The repo supports the practical benefit, but not a quantified cost metric.
- Avoid saying: **"We fully reproduced every race scenario."** The repo supports repeatable tests, bench tests, GPS/platform tests, and preparation for race tasks, but not a full race simulator claim.

## Innovation Pillar 2: Data-Centric Maritime Perception Pipeline

The perception innovation is data-centric: the team did not only train a model, but structured the dataset and augmentations around maritime conditions.

Verified elements from the repo:

- the Vision module detects maritime navigation elements, mainly fixed buoys, moving buoys, and docking-related elements;
- the pipeline includes data collection, sorting, annotation, training, inference tests, export preparation, and Jetson deployment preparation;
- annotation was performed with CVAT to produce labels usable by YOLO;
- the model training used YOLO26;
- augmentations were adapted to maritime scenes to improve robustness against variations of light, reflections, noise, motion blur, and scale changes;
- the collected images targeted close and distant buoys, reflections, different light conditions, different viewing angles, maritime backgrounds, and docking elements;
- annotation rules accounted for small objects, reflections, and partially visible objects when still identifiable.

For the Innovation Prize story, the key idea is:

**The augmentations are not just a way to create more images. They are a controlled way to teach the model to generalize to MEBC-like maritime perception conditions.**

Supported maritime conditions to mention:

- sunlight and lighting changes;
- reflections on water;
- different camera or viewing angles;
- close and distant buoys, represented as scale changes;
- partially visible buoys;
- maritime and water backgrounds;
- visual degradation such as noise and motion blur.

Use "MEBC-like" or "Monaco-like maritime conditions" as a goal and design direction, not as a claim that every Monaco condition has already been quantitatively validated.

## Innovation Pillar 3: BlueBoat-Adapted DWA Local Planner

The navigation-algorithm innovation verified in the adjacent BlueBoat code workspace is a **Dynamic Window Approach (DWA) local planner adapted to the BlueBoat autonomous mode**.

The planner does not only follow a static waypoint list. It evaluates short-horizon motion commands that the boat can physically reach, predicts the resulting trajectories, scores them, and selects the best command for the next control step.

Verified algorithm facts:

- `BlueBoat/AutonomousMode/configs/base.yml` sets `planner: dwa`;
- `BlueBoat/AutonomousMode/src/path_planning2.py` imports `src.path_planning_utils.dwa2` when `parameters.planner == "dwa"`;
- `path_planning2.py` calls `planner.dwa_control(...)` when the selected planner is DWA;
- the DWA state used by `path_planning2.py` is local boat position `x, y`, heading, linear speed, and angular speed;
- the boat GPS position is converted to local metric coordinates with `utils.gps_to_local(...)`;
- `BlueBoat/AutonomousMode/src/path_planning_utils/dwa2.py` defines the DWA implementation.

For each planning step, the algorithm:

1. builds a dynamic window from minimum and maximum speed, maximum yaw rate, acceleration and deceleration limits, and maximum yaw acceleration;
2. samples candidate linear speeds and yaw rates inside that reachable window;
3. predicts a trajectory for each candidate command over the configured time horizon;
4. scores each predicted trajectory with waypoint/target heading cost, speed cost, obstacle cost, and polygon boundary cost;
5. selects the command with the lowest total cost;
6. writes the selected command to shared state as `command_pp`, `velTarget_ms`, `omegaTarget_rads`, `command_point_pp`, `latTarget_deg`, and `lonTarget_deg`.

Why this is a navigation innovation:

- it uses BlueBoat vehicle limits from configuration;
- it plans in a local metric frame converted from GPS;
- it evaluates feasible boat motions instead of directly jumping from waypoint to waypoint;
- it includes obstacle and navigation-boundary costs;
- it outputs both speed/yaw commands and a converted GPS target point.

Safe one-sentence claim:

> A BlueBoat-adapted DWA local planner samples feasible speed/yaw commands, predicts short-horizon trajectories, scores them against waypoint progress, speed, obstacles, and navigation boundaries, then outputs the selected command to the autonomous-mode shared state.

## Proof Points Available in the Repo and Code Workspace

### BlueBoat and Embedded Integration

- The project used the BlueBoat as a main test bench because access to the final chassis was late.
- The BlueBoat supported work on perception, communications, sensor and actuator integration, test procedures, and transition toward the Monaco boat.
- The AI integration on the BlueBoat is described as complete in the realization report.
- The network, Jetson, cameras, remote access, QGroundControl, and MAVLink communications are described as in place.
- Integration of real actuators and sensors on the BlueBoat is described as engaged to simulate the final boat and prepare the transition.

### Vision and Dataset Pipeline

- The Vision module is designed around Jetson AGX Orin, ZED X One cameras, YOLO/ZED inference, and a dataset/training workflow.
- The realization report documents data collection, CVAT annotation, YOLO26 training, inference tests, and export preparation.
- The best documented detection results include a `yolo26_maritime2` training run with mAP50 up to `0.99253` and mAP50-95 up to `0.88753` across the reported best detection results.
- The best model prediction summary reports `467` predictions with an average confidence score of `0.93135`.

### Navigation Algorithm

- `planner: dwa` is selected in the BlueBoat autonomous-mode base configuration.
- `path_planning2.py` builds the DWA state from local position, heading, linear speed, and angular speed.
- GPS latitude/longitude is converted into a local metric frame before planning.
- `dwa2.py` computes a dynamic window from physical speed, yaw-rate, acceleration, deceleration, and yaw-acceleration constraints.
- The planner samples candidate commands, predicts trajectories, scores them, and returns the selected speed/yaw command plus the predicted trajectory.
- The selected command is published into shared state for downstream autonomous-mode control.

### Scope Limits

- The documented quantitative validation is mainly for buoy detection classes.
- Docking was prepared and annotated, but the repo explicitly says it should not be presented as quantitatively validated with the same metrics.
- The repo supports robustness-oriented augmentations, but it does not provide a separate ablation study proving the exact contribution of each augmentation.
- The current DWA path in `path_planning2.py` does not prove that live vision detections are active obstacles, because the append line from `detected_objects_world` into `self.buoysEst_dwa` is commented out.

## Suggested 2-Minute Video Structure

### 0:00-0:20 - Problem

"For the MEBC AI Class, we need an autonomous boat that can perceive, decide, and act in a real maritime environment. But the final boat was not available from the beginning, and real buoy data was limited."

Visuals:

- BlueBoat;
- final boat concept or Hobie Cat base;
- camera/Jetson close-up;
- examples of buoy images.

### 0:20-0:50 - Innovation Overview

"Our innovation is a data-centric simulation-to-real pipeline. We combine a real BlueBoat validation platform with a maritime perception dataset and augmentations designed for sea conditions."

Visuals:

- simple pipeline diagram: data -> augmentation -> YOLO26 -> Jetson/ZED -> BlueBoat -> final boat;
- CVAT screenshots;
- training/inference screenshots.

### 0:50-1:20 - BlueBoat Validation

"The BlueBoat allowed us to validate architecture, communication, perception integration, and control interfaces before relying on the real competition boat. It reduced dependency on the final chassis, avoided unnecessary risk in early tests, and made repeatable validation possible."

Visuals:

- BlueBoat with Jetson/cameras;
- QGroundControl;
- MAVLink or BlueOS screens;
- test bench or platform tests.

### 1:20-1:50 - Maritime Data Pipeline

"On the perception side, we designed the training process around maritime variability: changing light, reflections, viewing angle, buoy scale, partial visibility, water backgrounds, noise, and motion blur. The objective was not just more data, but better generalization to MEBC-like conditions."

Visuals:

- annotated buoy images;
- augmentations or varied examples;
- YOLO detection output.

### 1:50-2:00 - Navigation and Impact

"For navigation, the BlueBoat autonomous mode uses a DWA local planner. It samples feasible speed and yaw commands, predicts short-horizon trajectories, scores them against waypoints, speed, obstacles, and boundaries, then outputs the selected command to the shared autonomous state. This creates a practical bridge from AI development to real autonomous navigation."

Visuals:

- DWA trajectory or planner screenshot;
- BlueBoat test setup;
- final boat preparation.

## Slide Preparation Notes

Recommended slide titles:

1. **The Challenge: Autonomy Before the Final Boat**
2. **Our Innovation: Data-Centric Simulation-to-Real Pipeline**
3. **BlueBoat as a Real Validation Platform**
4. **Maritime Augmentations for Buoy Detection**
5. **DWA Local Planning for Feasible Boat Motion**
6. **Proof of Concept and MEBC Value**

Key phrases to reuse:

- "from dataset to embedded validation";
- "robust buoy detection under maritime variability";
- "BlueBoat as a bridge between offline AI and real competition hardware";
- "repeatable validation before high-risk full-scale testing";
- "augmentations designed around the physics and visuals of maritime perception";
- "DWA local planning turns waypoints into feasible short-horizon boat commands."

## Claims to Avoid or Soften

Avoid unsupported absolute claims:

- "The system is fully race-ready."
- "We proved generalization to all Monaco conditions."
- "We reduced testing cost by a measured percentage."
- "We simulated every race scenario."
- "Docking detection is quantitatively validated at the same level as buoy detection."
- "Live vision detections are already used as DWA obstacles."

Use supported wording instead:

- "The system provides a proof of concept installed and tested on the BlueBoat."
- "The pipeline is designed to improve generalization to MEBC-like maritime conditions."
- "The BlueBoat reduced dependency on the final chassis and enabled earlier validation."
- "The platform supports repeatable bench and integration tests before full-scale trials."
- "Docking elements were prepared and annotated, while the strongest quantitative results currently concern buoy detection."
- "The DWA obstacle list currently includes configured buoys and a moving test buoy; live vision objects are converted to local coordinates but not appended to the DWA obstacle list in the current `path_planning2.py` version."

## Verified Facts From Repo and Code Workspace

### `InnovationVideo/MEBC2026 - TechTalk Prizes (1) (1).pdf`

- Innovation Prize requires a maximum 2-minute pitch video.
- It also requires technical documentation.
- Criteria include novelty, problem solving and value creation, market potential, feasibility, scalability, and proof of concept.

### `RapportFinal/rapport.tex`

- The project targets the Monaco Energy Boat Challenge 2026 AI class.
- The goal is an autonomous system able to perceive, decide, and control the vehicle.
- Late access to the final chassis was a central constraint.
- The BlueBoat was used as the main test bench to maintain software progress and prepare transition to the Monaco boat.
- The BlueBoat supported work on perception, communications, sensor/actuator integration, test procedures, and architecture choices.

### `Réalisation/dossier/dossierRéalisation.tex`

- The Vision work covers environment setup, dataset creation, annotation, detection model training, inference tests, export, and Jetson/ZED integration preparation.
- Images were selected to cover close and distant buoys, reflections, different light conditions, different viewing angles, maritime backgrounds, and docking elements.
- CVAT was used for annotation.
- YOLO26 was trained with augmentations adapted to maritime scenes.
- Augmentations targeted robustness to light variation, reflections, noise, motion blur, and scale changes.
- The BlueBoat was modified with Jetson, cameras, power supply, and network integration.
- QGroundControl was selected for supervision and rapid mode changes during real-condition tests.
- The AI integration phase on the BlueBoat is described as complete.
- Integration of real actuators and sensors on the BlueBoat is described as underway to simulate the final boat.

### `ManuelVision/manuelVision.tex`

- The Vision module perceives the maritime environment and detects buoys, obstacles, and useful navigation elements.
- Hardware includes Jetson AGX Orin and Stereolabs ZED X One cameras.
- The module uses a YOLO/ZED pipeline.
- Outputs include object detections, class, confidence score, and, when ZED depth is available, estimated 3D position or approximate distance.
- The dataset/training section documents classes and training files used for the model workflow.

### Adjacent BlueBoat code workspace: `../IABoat/BlueBoat/AutonomousMode`

- `configs/base.yml` selects `planner: dwa`.
- `src/path_planning2.py` selects `src.path_planning_utils.dwa2` when `parameters.planner == "dwa"`.
- `src/path_planning2.py` calls `planner.dwa_control(...)` and updates shared-state command fields.
- `src/path_planning2.py` converts GPS coordinates to local metric coordinates with `utils.gps_to_local(...)`.
- `src/path_planning_utils/dwa2.py` implements dynamic-window calculation, command sampling, trajectory prediction, obstacle cost, polygon-boundary cost, and best-command selection.
- `configs/boats/blueboat.yml` defines BlueBoat vehicle limits used by the DWA configuration, including speed, yaw-rate, acceleration, deceleration, and yaw-acceleration limits.
