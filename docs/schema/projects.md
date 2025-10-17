# project_info.yaml
```
project_name: Project Name
ethics: integer
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
data_path: "./XX_Data/"
program: Program Name
members:
  - First Member
  - ...
location:
  - name: NC Lab, CCCare, Manulife Center, ...
participants:
  groups:
    - label: Group Label
      n: integer
      attributes: ["Healthy", "Control", "PD", "Freezer", "Non-freezer", ...]
data_sources:
  - category: motion
    modality: imu, gait-carpet, mocap
    name: Shimmer, Opals, ...
  - category: physio
    modality: cardiac, respiratory, pupils, eda, emg
    name: Shimmer, Bittium, ...
  - category: neuro
    modality: func, anat, dwi, nirs, eeg
    name: NIRx, ...
  - category: clinic
    modality: questionnaire
    name: FoG-Q, PDQ, UPDRS, ...
  - category: misc
    modality: beh, video
    name: GoPro, ...
outputs:
  - name: Output Title
    type: Publication, Pre-print, Conference poster, Conference presentation, ...
    url: https://doi.org/
  - ...
```

!!! note "Important"
    The ```data_path``` field should be relative to the project folder itself (i.e. the data subfolder name within the project folder).

!!! note "Important"
    The listed ```program``` should match a name in the [programs_info.yaml](programs.md) file located in the *programs* subfolder.

!!! note "Important"
    All listed ```members``` should match a name in the [members_info.yaml](members.md) file located in the *people* subfolder.