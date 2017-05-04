class STATE:
    """
    This stores all the states that the reimbursement form can be in
    """
    SUBMITTED = 'Submitted'
    VERIFIED_BY_DA = 'Verified by Dealing Assistant'
    APPROVED_BY_MS = 'Verified by Medical Superintendent'
    APPROVED_BY_DR = 'Approved by Deputy Registrar'
    APPROVED_BY_SrAO = 'Approved by Senior Audit Officer.'
    APPROVED_BY_R = 'Approved by Registrar'
    AMOUNT_TRANSFERRED = 'Reimbursed'
    REJECT = 'Rejected'

    def __init__(self):
        pass