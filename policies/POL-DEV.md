# POL-DEV: Device Compliance Standard

- Version: 2.2
- Effective date: 2026-03-01
- Owner: Endpoint Engineering
- Company: Northwind Ltd (fictional; synthetic training data)

### POL-DEV-1 Scope

This standard applies to every device used to access Northwind corporate applications.

### POL-DEV-2.1 Disk encryption

Disk encryption (BitLocker on Windows, FileVault on macOS) must be enabled.

### POL-DEV-2.2 Operating system updates

Operating system security updates must be installed within 14 days of release for critical updates and within 30 days for all others.

### POL-DEV-2.3 Endpoint protection

Endpoint protection must be active and its signatures no more than 7 days old.

### POL-DEV-2.4 Check-in

A managed device must check in to device management at least every 30 days.

### POL-DEV-2.5 Jailbroken or rooted devices

A jailbroken or rooted device is never compliant.

### POL-DEV-3.1 Grace period

A newly non-compliant device has a grace period of 7 days from first detection before conditional access blocks it from corporate applications.

### POL-DEV-3.2 After the grace period

After the grace period the device is blocked until it is compliant again. The user remediates the cause as described in section 4.

### POL-DEV-4.1 Self-service remediation

Users can install pending updates, restart the device, and open Company Portal and choose Check status or Sync. Endpoint protection signatures update through Windows Security.

### POL-DEV-4.2 Encryption

Users cannot enable disk encryption on a company device themselves because the recovery key must be escrowed. The Service Desk arranges assisted remediation through Endpoint Engineering.

### POL-DEV-4.3 Devices not checking in

A device that has not checked in for more than 30 days should connect to the corporate network or VPN and sync in Company Portal. A device that has not checked in for more than 60 days may be retired and must be re-enrolled by the Level 2 Service Desk.

### POL-DEV-5.1 Personal (BYOD) devices

Personal mobile devices may access Outlook and Teams only with app protection (MAM) in place and must not be used for Confidential or Restricted data. Personal laptops cannot be enrolled.

### POL-DEV-5.2 Agency and contractor devices

Contractor or agency devices must be enrolled in device management, otherwise the contractor is limited to browser-only access to Internal content.

### POL-DEV-6.1 Lost or stolen devices

A lost or stolen device must be reported to IT Security within 1 hour of discovery. Only IT Security can remotely wipe or lock a device.

### POL-DEV-6.2 Jailbreak detection

If a jailbroken or rooted device is detected the case is escalated to IT Security. Details of the detection are not shared in the ticket.
