# project_info.yaml
```
project_name: Project Name
ethics: integer
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
data_path: "./XX_Data/"
program: Program Name
members:
  - Member Name
  - ...
location:
  - name: NC Lab, ...
participants:
  groups:
    - label: Group Label
      total: 0
      collected: 0
      attributes: ["attribute one", "attribute two", ...]
data_sources:
  - category: motion
    modality: imu, gait-carpet, mocap
    device: Shimmer, Opals, ...
  - category: physio
    modality: cardiac, respiratory, pupils, eda, emg
    device: Shimmer, Bittium, ...
  - category: neuro
    modality: func, anat, dwi, nirs, eeg
    device: NIRx, ...
  - category: clinic
    modality: clinometrics, demographics
    device: FoG-Q, PDQ, UPDRS, ...
  - category: misc
    modality: beh, video
    device: GoPro, ...
outputs:
  - name: Output Title
    type: Publication, Pre-print, Conference poster, Conference presentation, ...
    url: https://doi.org/
    date: YYYY-MM-DD
  - ...
```

!!! note "Important"
    The ```data_path``` field should be relative to the project folder itself (i.e. the data subfolder name within the project folder).

!!! note "Important"
    The listed ```program``` should match a program name in the [programs_info.yaml](programs.md) files located in the *lab-administration/Programs* subfolder.

!!! note "Important"
    All listed ```members``` should match a member name in the [members_info.yaml](members.md) file located in the *people* subfolder.
