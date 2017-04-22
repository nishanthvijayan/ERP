class STATE:
    """
    This stores all the states that the reimbursement form can be in
    """
    SUBMITTED = 'SUBMITTED'
    VERIFIED_BY_DA = 'VERIFIED_BY_DA'
    APPROVED_BY_MS = 'APPROVED_BY_MS'
    APPROVED_BY_AR = 'APPROVED_BY_AR'
    APPROVED_BY_DR = 'APPROVED_BY_DR'
    APPROVED_BY_SrAO = 'APPROVED_BY_SrAO'
    APPROVED_BY_R = 'APPROVED_BY_R'
    AMOUNT_TRANSFERRED = 'AMOUNT_TRANSFERRED'

    def __init__(self):
        pass

STATE_CHOICES = (
    (STATE.SUBMITTED, 'Submitted by employee', 'Medical'),
    (STATE.VERIFIED_BY_DA, 'Verified by Dealing Assistant', 'Medical'),
    (STATE.APPROVED_BY_MS, 'Approved by Medical Superintendent', 'Medical'),
    (STATE.APPROVED_BY_AR, 'Approved by Assistant Registrar', 'Medical'),
    (STATE.APPROVED_BY_DR, 'Approved by Deputy Registrar', 'Medical'),
    (STATE.APPROVED_BY_SrAO, 'Approved by Senior Audit Officer', 'Medical'),
    (STATE.APPROVED_BY_R, 'Approved by Registrar', 'Medical'),
    (STATE.AMOUNT_TRANSFERRED, 'Amount transferred by Accounts Department', 'Medical'),
)

# STATE_CHOICES = (
#     (STATE.SUBMITTED, 'Submitted by employee', 'To be verified by Dealing Assistant'),
#     (STATE.VERIFIED_BY_DA, 'Verified by Dealing Assistant', 'To be approved by Medical Superintendent'),
#     (STATE.APPROVED_BY_MS, 'Approved by Medical Superintendent', 'To be approved by Assistant Registrar'),
#     (STATE.APPROVED_BY_AR, 'Approved by Assistant Registrar', 'To be approved by Deputy Registrar'),
#     (STATE.APPROVED_BY_DR, 'Approved by Deputy Registrar', 'To be approved by Senior Audit Officer'),
#     (STATE.APPROVED_BY_SrAO, 'Approved by Senior Audit Officer', 'Butterfly'),
#     (STATE.APPROVED_BY_R, 'Approved by Registrar', 'Amount to be transferred in bank account'),
#     (STATE.AMOUNT_TRANSFERRED, 'Amount transferred by Accounts Department', ''),
# )
