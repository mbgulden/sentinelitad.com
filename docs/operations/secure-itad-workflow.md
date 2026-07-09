# Sentinel Secure ITAD Workflow and Tooling Plan

**Purpose:** turn the website trust promise into a real operating workflow. This is the working baseline, not a public certification claim.

## Service states

| State | Public claim allowed | Evidence required |
|---|---|---|
| Intake only | Pickup receipt / custody handoff | Signed receipt, photos, asset count, exceptions |
| Media segregation | Data-bearing media handled separately | Asset/media log, labels, sealed container/bin notes |
| Software sanitization | Sanitized only when actually completed and verified | Tool output, serial/WWN, method, verification result, operator, timestamp |
| Physical destruction | Destroyed only when actually performed or documented by downstream partner | Photos/video, destruction log, downstream certificate if partner-performed |
| Downstream recycling | Routed through downstream partner | Partner receipt/certificate, material class, weight/count where available |

## Initial tooling stack to build/test

Open-source/commodity baseline for the garage lab:

- Linux wiping station with hot-swap SATA/SAS/NVMe support.
- `smartmontools` for device identity/health: `smartctl -a /dev/sdX`.
- `nvme-cli` for NVMe identity/sanitize where supported: `nvme id-ctrl`, `nvme sanitize`, `nvme format`.
- `hdparm` for ATA security where appropriate: `hdparm -I`, secure erase support checks.
- `sg3-utils` for SCSI/SAS identity and sanitize support where applicable.
- `nwipe` or equivalent for HDD overwrite workflows where firmware sanitize is not appropriate.
- Barcode/QR labels mapped to the asset/media log.
- PDF generator for certificates/reports from CSV/SQLite job data.

Commercial tooling to evaluate before stronger public claims:

- Blancco Drive Eraser.
- BitRaser Drive Eraser.
- KillDisk Industrial.

## Operating workflow

1. **Scope request**
   - Capture company, contact, pickup location, material classes, media sensitivity, stairs/loading constraints, desired documents, and insurance/additional-insured needs.

2. **Pickup / chain-of-custody**
   - Use `docs/templates/printable-pickup-receipt.html`.
   - Photograph staged material where appropriate.
   - Mark data-bearing media as present/absent/unknown.

3. **Intake**
   - Assign job ID: `SIAL-YYYYMMDD-###`.
   - Assign asset IDs and media IDs.
   - Fill `docs/templates/sample-asset-media-log.csv` fields or a future SQLite-backed form.
   - Separate media into sanitized / destroy / hold / return bins using the sticker labels.

4. **Triage**
   - Reuse/resale candidates: servers, workstations, RAM, CPUs, SSDs, NICs, GPUs, monitors.
   - Media: wipe candidate, physical destruction, return to client, or downstream partner.
   - E-waste/scrap: downstream partner route.

5. **Sanitization / destruction**
   - Record manufacturer, model, serial/WWN, firmware if available.
   - Record exact method and tool output.
   - Verify result; do not treat “command started” as proof.
   - Failed media gets an exception note and a destroy/downstream path.

6. **Disposition package**
   - Pickup receipt.
   - Asset/media log.
   - Certificate/report from real evidence.
   - Downstream partner documentation where applicable.
   - Insurance certificate/additional insured documents when requested/approved.

## Certificate/report fields

Minimum fields for any real certificate:

- certificate ID and job ID
- client name and service date
- asset/media ID
- manufacturer/model
- serial number / WWN
- media capacity/type
- method used
- NIST 800-88 category only if the process truly matches it
- tool/log reference and hash
- verification result
- exception notes
- operator and signature/date
- downstream partner documentation reference if applicable

## Website wording implication

Until the toolchain is installed, tested, and sample evidence packages exist, public copy should say “data-bearing media handled separately” and “documents available based on service performed,” not “certified data destruction.” Yes, it is less sexy. So are subpoenas.
