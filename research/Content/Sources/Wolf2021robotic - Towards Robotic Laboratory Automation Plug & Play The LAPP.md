---
aliases: []
type: "source"
title: "Towards Robotic Laboratory Automation Plug & Play: The \"LAPP\" Framework"
citekey: "Wolf2021robotic"
doi: "10.48550/arXiv.2106.10129"
arxiv: "2106.10129"
year: 2021
publication_type: "preprint"
url: "https://arxiv.org/abs/2106.10129"
keywords: []
status: "to-read"
rating: 0
authors: []
authors_unresolved: ["Ádám Wolf", "David Wolton", "Josef Trapl", "Julien Janda", "Stefan Romeder-Finger", "Thomas Gatternig", "Jean-Baptiste Farcet", "Péter Galambos", "Károly Széll"]
sha256: ["37ce87bdc3e1f847906ac455f8427516f6560349ae98dbcb2d36f89f3f197236"]
pdf: "Content/Papers/Wolf2021robotic.pdf"
topics: ["[[Ampliación]]"]
cited_in: ["[[04_huecos_y_ampliacion]]"]
created: "2026-09-18"
created_by: "ingest-writer@25466ccf498f"
checked_by: "ingest-checker@a741699004ec"
ingested: "2026-09-18"
claims: 61
---

📄 PDF: [[Wolf2021robotic.pdf]]

> [!abstract] One-sentence summary
> A perspective paper that surveys industrial and laboratory automation standards and proposes LAPP, where each device carries a barcode and a fiducial marker so a mobile manipulator can locate it, fetch its interface and action primitives from a cloud database, and operate it plug & play.

## Abstract

Increasing the level of automation in pharmaceutical laboratories and production facilities plays a crucial role in delivering medicine to patients. However, the particular requirements of this field make it challenging to adapt cutting-edge technologies present in other industries. This article provides an overview of relevant approaches and how they can be utilized in the pharmaceutical industry, especially in development laboratories. Recent advancements include the application of flexible mobile manipulators capable of handling complex tasks. However, integrating devices from many different vendors into an end-to-end automation system is complicated due to the diversity of interfaces. Therefore, various approaches for standardization are considered in this article, and a concept is proposed for taking them a step further. This concept enables a mobile manipulator with a vision system to "learn" the pose of each device and - utilizing a barcode - fetch interface information from a universal cloud database. This information includes control and communication protocol definitions and a representation of robot actions needed to operate the device. In order to define the movements in relation to the device, devices have to feature - besides the barcode - a fiducial marker as standard. The concept will be elaborated following appropriate research activities in follow-up papers. (arXiv)

## 🧠 Key ideas (atomic)

- This perspective paper surveys technologies from other fields that can benefit pharmaceutical companies, focusing especially on mobile robotics in R&D laboratories. (Wolf et al., 2021) `ev:asserted` p. 4 ^wolf2021robotic-001
- The goal of the proposed concept is to ease system integration of mobile robotics through no-configuration, no-teaching, Plug & Play functionality. (Wolf et al., 2021) `ev:asserted` p. 4 ^wolf2021robotic-002
- The authors consider the present article a high-level overview of existing approaches that also outlines the proposed framework concept. (Wolf et al., 2021) `ev:asserted` p. 25 ^wolf2021robotic-003
- Eroom's law states that the number of drugs per billion US$ is declining logarithmically, a reverse curve to Moore's law. (Wolf et al., 2021) `ev:cited` p. 3 ^wolf2021robotic-004
- The authors cite that approximately two thirds of academic research fails to be repeated by the very few peers who attempt it. (Wolf et al., 2021) `ev:cited` p. 3 ^wolf2021robotic-005
- In pharmaceuticals, strict validation processes make adapting new technologies slower, which changes the cost/benefit ratio relative to less regulated industries. (Wolf et al., 2021) `ev:asserted` p. 3 ^wolf2021robotic-006
- The authors state that static robots have only limited application in pharmaceutical manufacturing, unlike recently developed mobile industrial robots. (Wolf et al., 2021) `ev:asserted` p. 3 ^wolf2021robotic-007
- Most laboratory devices are still designed for manual operation, where a human operator loads samples, sets parameters, starts the process, then unloads. (Wolf et al., 2021) `ev:asserted` p. 4 ^wolf2021robotic-008
- Mechanical interfaces that would let an independent manipulator load samples into a laboratory device are not commonly present, according to the authors. (Wolf et al., 2021) `ev:asserted` p. 4 ^wolf2021robotic-009
- The Reference Architectural Model Industrie 4.0 provides communication structures with a common language for integrating participants such as robots. (Wolf et al., 2021) `ev:cited` p. 5 ^wolf2021robotic-010
- Introduced in 2008, OPC UA has since become a worldwide standard for client-server communication with industrial equipment. (Wolf et al., 2021) `ev:cited` p. 6 ^wolf2021robotic-011
- In the Asset Administration Shell concept, each physical asset, such as robots, sensors, analytical devices or workpieces, has its own admin shell representation. (Wolf et al., 2021) `ev:cited` p. 6 ^wolf2021robotic-012
- The authors suggest a similar asset-shell approach can be applied to laboratory automation, where samples are considered the most important assets. (Wolf et al., 2021) `ev:asserted` p. 6 ^wolf2021robotic-013
- Collaborative robots have to avoid collisions with humans or at least minimise collision forces, as specified in ISO/TS 15066:2016. (Wolf et al., 2021) `ev:cited` p. 7 ^wolf2021robotic-014
- Safety requirements and regulations for mobile robots are even less established than for collaborative robots, according to the authors. (Wolf et al., 2021) `ev:asserted` p. 7 ^wolf2021robotic-015
- Autonomous mobile robots do not rely on purpose-mounted external references; instead they use on-board sensors to perceive their surroundings. (Wolf et al., 2021) `ev:cited` p. 8 ^wolf2021robotic-016
- Unlike arm-less AGVs or AMRs, mobile manipulators can operate equipment designed for humans, which gives them a greater scope of operation. (Wolf et al., 2021) `ev:asserted` p. 8 ^wolf2021robotic-017
- Many laboratory tasks, such as measuring out a certain amount of powder from a container, require dexterity not yet achievable by robots. (Wolf et al., 2021) `ev:asserted` p. 9 ^wolf2021robotic-018
- Most stand-alone automated laboratory devices are not optimized for being integrated into an overlaying automation system, according to cited work. (Wolf et al., 2021) `ev:cited` p. 9 ^wolf2021robotic-019
- The authors state that lights-out laboratory operation cannot be achieved with the current state of technology in most cases. (Wolf et al., 2021) `ev:asserted` p. 9 ^wolf2021robotic-020
- Chu et al. interfaced an LC-MS system through a basic C# script using simulated mouse clicks with keyboard inputs. (Wolf et al., 2021) `ev:cited` p. 11 ^wolf2021robotic-021
- The SiLA standard defines laboratory devices as servers with a predefined set of features that a client can call. (Wolf et al., 2021) `ev:cited` p. 11 ^wolf2021robotic-022
- A SiLA feature definition for mobile manipulators already exists, containing services for battery control, calibration, gripper control, robot control, teaching. (Wolf et al., 2021) `ev:cited` p. 11 ^wolf2021robotic-023
- The LADS initiative, launched in 2020 by Spectaris, is developing a laboratory-specific information model built upon the OPC-UA protocol. (Wolf et al., 2021) `ev:cited` p. 12 ^wolf2021robotic-024
- The authors consider production-near environments such as QC more suitable for LADS, whereas SiLA is rather aimed at R&D labs. (Wolf et al., 2021) `ev:asserted` p. 12 ^wolf2021robotic-025
- The Universal Integration Knowledge Base was founded to act as a voluntary, community-sustained database of successful integration recipes with APIs. (Wolf et al., 2021) `ev:cited` p. 12 ^wolf2021robotic-026
- According to Fleischer et al., the biggest challenge for system integration in life science automation lies in decentralized, open systems. (Wolf et al., 2021) `ev:cited` p. 13 ^wolf2021robotic-027
- Integrating devices around stationary or rail-mounted robots introduces spatial constraints, which the authors say highly limits the flexibility of automated islands. (Wolf et al., 2021) `ev:cited` p. 14 ^wolf2021robotic-028
- The standard solution for mobile manipulators to locate graspable objects has become fiducial markers detected with a calibrated on-board camera. (Wolf et al., 2021) `ev:asserted` p. 14 ^wolf2021robotic-029
- Fraunhofer IPA's KEVIN combines a Care-o-bot 4 mobile platform, a PreciseFlex arm, with a vision system capable of localizing fiducial markers. (Wolf et al., 2021) `ev:cited` p. 15 ^wolf2021robotic-030
- Burger et al. used a KUKA iiwa mobile manipulator for conducting photocatalysis experiments within a ten-dimensional space. (Wolf et al., 2021) `ev:cited` p. 15 ^wolf2021robotic-031
- The authors conclude that a mobile platform with a robot arm plus fiducial-based pose detection is already well established in laboratory automation. (Wolf et al., 2021) `ev:asserted` p. 15 ^wolf2021robotic-032
- Mobile manipulators might not reach the speed of humans, but they can get closer to human flexibility than specialized stationary robots. (Wolf et al., 2021) `ev:asserted` p. 15 ^wolf2021robotic-033
- In Table 1, the authors rate throughput as high for stationary robots, low for mobile manipulators, middle for humans. (Wolf et al., 2021) `ev:asserted` p. 16 ^wolf2021robotic-034
- In Table 1, the authors rate flexibility as high for mobile manipulators or humans, but low for stationary robots. (Wolf et al., 2021) `ev:asserted` p. 16 ^wolf2021robotic-035
- A mobile manipulator could support remote 24/7 monitoring, letting stand-by personnel drive it to an error and sometimes resolve it by telemanipulation. (Wolf et al., 2021) `ev:asserted` p. 16 ^wolf2021robotic-036
- The TECAN Freedom Evo manipulator arm has 0.5 mm specified, whereas the PreciseFlex SCARA arm is given a 0.09 mm value. (Wolf et al., 2021) `ev:reported` p. 16 ^wolf2021robotic-037
- The precision of a mobile robot on its own lies around 50 mm, which has to be improved by additional position detection methods. (Wolf et al., 2021) `ev:asserted` p. 16 ^wolf2021robotic-038
- The authors state that a precision in position of around 1 mm with an angle precision around 1-2 deg is desired. (Wolf et al., 2021) `ev:asserted` p. 17 ^wolf2021robotic-039
- Garrido-Jurado et al. propose ArUco, a method for generating and detecting fiducial markers, naming robot localization among its application fields. (Wolf et al., 2021) `ev:cited` p. 17 ^wolf2021robotic-040
- Chu et al. propose the Motion Elements framework, a modular robot motion representation, specially for automating a sample preparation workflow. (Wolf et al., 2021) `ev:cited` p. 17 ^wolf2021robotic-041
- In the authors' list of limitations ordered by severity, the first is lacking standards for devices, consumables, mechanical interfaces and regulations. (Wolf et al., 2021) `ev:asserted` p. 17 ^wolf2021robotic-042
- The authors note that dexterous gripping is still considered an immature technology, which limits the adaptability of laboratory robots. (Wolf et al., 2021) `ev:asserted` p. 18 ^wolf2021robotic-043
- Identifying and localizing laboratory devices by robots is described by the authors as not yet a well-established capability. (Wolf et al., 2021) `ev:asserted` p. 18 ^wolf2021robotic-044
- The authors describe laboratory devices as not robot-ready, being self-contained proprietary solutions that lack automatic lids or doors. (Wolf et al., 2021) `ev:asserted` p. 18 ^wolf2021robotic-045
- A LAPP-enabled device has to feature two optical tags on its front face: a 1D or 2D barcode plus a fiducial marker. (Wolf et al., 2021) `ev:asserted` p. 19 ^wolf2021robotic-046
- The barcode lets a robot with a vision system fetch device-specific information from an online database such as the Universal Integration Knowledge Base. (Wolf et al., 2021) `ev:asserted` p. 19 ^wolf2021robotic-047
- The authors name websocket, REST-API, Graph-QL or gRPC as web technologies for database communication, noting gRPC is also used by SiLA. (Wolf et al., 2021) `ev:asserted` p. 19 ^wolf2021robotic-048
- Under LAPP, an initial, fully autonomous discovery procedure is intended to let a mobile robot operate in a newly installed laboratory. (Wolf et al., 2021) `ev:asserted` p. 21 ^wolf2021robotic-049
- In the LAPP sequence, the robot first generates a map with SLAM, then detects each device pose using its fiducial marker. (Wolf et al., 2021) `ev:asserted` p. 21 ^wolf2021robotic-050
- In the LAPP sequence, the scheduler requests device information from the cloud database, then instantiates a digital twin that it keeps updated. (Wolf et al., 2021) `ev:asserted` p. 21 ^wolf2021robotic-051
- The authors consider the LAPP framework protocol agnostic, meaning that multiple different technical solutions would be suitable for its functionality. (Wolf et al., 2021) `ev:asserted` p. 23 ^wolf2021robotic-052
- As example building blocks, the authors name UniteFlow for scheduling, SiLA for device interfacing, ROS as robot middleware, ArUco for markers. (Wolf et al., 2021) `ev:asserted` p. 23 ^wolf2021robotic-053
- The authors introduce LAPP Action Primitives, robot motions defined in the marker coordinate system for operating a device with an external robot. (Wolf et al., 2021) `ev:asserted` p. 23 ^wolf2021robotic-054
- The authors state that the possibility of manual adjustments and calibration should be kept open despite out-of-the-box action primitives. (Wolf et al., 2021) `ev:asserted` p. 23 ^wolf2021robotic-055
- The authors argue that the standard is as good as its level of acceptance, requiring industry-wide involvement to reach its potential. (Wolf et al., 2021) `ev:asserted` p. 24 ^wolf2021robotic-056
- In the ballroom manufacturing concept, the authors expect mobile-manipulator-based automated systems to gain importance over conveyor-belt layouts. (Wolf et al., 2021) `ev:asserted` p. 24 ^wolf2021robotic-057
- A planned article series will first focus on the LAPP-AP concept, representing robot movements in relation to the marker coordinate frame. (Wolf et al., 2021) `ev:asserted` p. 25 ^wolf2021robotic-058
- Future work will evaluate end-effector possibilities such as tool-changers, multi-tools or universal grippers for operating a variety of devices. (Wolf et al., 2021) `ev:asserted` p. 25 ^wolf2021robotic-059
- The authors state that existing standardization initiatives lack sufficient acceptance to effectively enable a Plug & Play laboratory integration experience. (Wolf et al., 2021) `ev:asserted` p. 26 ^wolf2021robotic-060
- For the action primitive database, the authors state robotic actions have to be represented in a structured, modular, parametric fashion. (Wolf et al., 2021) `ev:asserted` p. 26 ^wolf2021robotic-061

## 🎯 Contributions

## 📖 Glossary

- **LAPP** — Laboratory Automation Plug & Play: barcode plus fiducial marker device integration concept for mobile robots.
- **LAPP-AP** — Action primitives: device-specific robot motions defined in the fiducial marker's coordinate frame.
- **MoMa** — Mobile manipulator: autonomous mobile base carrying one or more robot arms and sensors.
- **AMR** — Autonomous mobile robot navigating with on-board sensors instead of external guides.
- **SiLA** — Standardization in Lab Automation: device-as-server communication and control standard for laboratories.
- **LADS** — OPC-UA-based laboratory device information model standard launched by Spectaris in 2020.
- **UIKB** — Universal Integration Knowledge Base: community database of device integration recipes and APIs.
- **Fiducial marker** — Printed 2D pattern whose pose a calibrated camera can estimate.
- **Asset Administration Shell** — Industrie 4.0 digital representation encapsulating all data about a physical asset.

## ❓ Open questions

- How should action primitives be represented concretely so they transfer across robots, grippers and vendors?
- Can fiducial-marker pose detection reach the desired 1 mm and 1-2 deg precision for mobile manipulation?
- Which end-effector strategy (tool-changer, multi-tool, universal gripper) best covers the variety of laboratory devices?
- How would device vendors be incentivised to publish action primitives and fit standard markers?
- How can LAPP be validated under GxP regulation and address the IT security concerns the authors list?
- How can dexterous tasks such as powder dosing, named as beyond current robots, be brought into the framework?

## 📝 Notes on reading

Read the arXiv v3 preprint (4 Nov 2021). This is a perspective/concept paper: no implementation, experiment or quantitative evaluation of LAPP is reported; almost all claims are `asserted` or `cited`.

Figure 1 (p. 22) is a diagram of the LAPP sequence connecting robot, devices, scheduler (e.g. UniteFlow), cloud database (e.g. UIKB) and digital twin; it could only be described.

Inconsistency: the text list on p. 21 orders the steps as (2) detect device pose with the fiducial marker, (3) read barcode, while the Figure 1 caption on p. 22 gives (2) detect barcode, (3) detect fiducial pose.

Table 1 (p. 16) is a qualitative High/Middle/Low comparison of stationary robot, MoMa and human for throughput, availability and flexibility; availability is rated High, Middle, Low respectively. Table 2 (p. 20) lists information to fetch and its utilization; its two-column layout was flattened in extraction but remains readable.

The precision figures (TECAN 0.5 mm, PreciseFlex 0.09 mm, mobile base around 50 mm) carry no reference in the text.

## Suggested new concepts

- Laboratory Automation Plug & Play (LAPP) — a named framework for marker-plus-barcode device onboarding by mobile robots, relevant to any vision-based lab robot.
- Action primitives in marker frames — representing device-operation motions relative to a fiducial marker is a reusable idea for robot skill transfer.
- Fiducial-marker pose detection for lab robots — the standard localization method in laboratory mobile manipulators per this survey.
- SiLA — the main laboratory device communication standard, recurring across lab automation sources.
- Mobile manipulator (MoMa) in laboratories — an established platform blueprint with its throughput and flexibility trade-offs.

## Por qué es relevante

- **[[04_huecos_y_ampliacion]]** — **H7.** Es la referencia citable sobre lectura de códigos de barras y marcadores fiduciales para identificar y localizar equipos en un laboratorio robotizado.

<!-- ingest-checker dropped 1 claim(s); see _harness/log/ingest.jsonl (claim-dropped) -->
