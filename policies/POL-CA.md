# POL-CA: Conditional Access and Lockout Guide

- Version: 1.4
- Effective date: 2025-06-10
- Owner: Head of Identity and Access, IT Security
- Company: Northwind Ltd (fictional; synthetic training data)

### POL-CA-1 Purpose

This guide explains why sign-ins are blocked and what the Service Desk can and cannot do about it.

### POL-CA-2.1 Reasons for a block

Sign-ins are blocked for five main reasons: sign-in from an unapproved country, a non-compliant device, a failed multi-factor authentication (MFA) challenge, a risky sign-in, or an account lockout.

### POL-CA-2.2 Approved countries

Approved countries are the United Kingdom, Ireland, Germany, India, the United States and the other EU and EEA states.

### POL-CA-2.3 Non-compliant devices

A non-compliant device is blocked from corporate applications after 3 days.

### POL-CA-3.1 Travel exceptions

Travel to a country that is not approved needs a travel exception. The request must be made at least 3 working days before travel, needs line manager approval, lasts at most 30 days and is granted by IT Security only.

### POL-CA-3.2 Service Desk role in travel

The Service Desk cannot add country exceptions. It collects the traveller's dates and destination and escalates to IT Security.

### POL-CA-4.1 Lost or replaced MFA device

A user with no registered second MFA method cannot recover access on their own. The Level 2 Service Desk verifies identity (line manager call-back and ID check) before issuing a Temporary Access Pass (TAP). The Service Desk agent and automated agents must not reset MFA or issue a TAP.

### POL-CA-4.2 Temporary Access Pass

A TAP is valid for 8 hours.

### POL-CA-5.1 Smart lockout

After 10 failed password attempts an account is locked for 30 minutes. The user can wait for the lockout to end or use self-service password reset (SSPR) if they have registered for it.

### POL-CA-5.2 Repeated lockouts

Repeated lockouts from unfamiliar IP addresses must be reported to IT Security.

### POL-CA-6.1 High-risk sign-ins

High-risk sign-ins are blocked automatically. The Service Desk must not unblock them or advise how to get round the block. The case is escalated to Security Operations immediately and the requester is told only that the matter is being looked into.

### POL-CA-7.1 New joiners

On the first day, once the line manager has confirmed the start, the Level 2 Service Desk issues a TAP for the first sign-in. The joiner registers MFA within 24 hours.
