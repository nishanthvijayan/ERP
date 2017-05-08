class STATE:
    """
    This stores all the states that the reimbursement form can be in
    """
    SUBMITTED = 'Submitted'
    APPROVED_BY_HOD = 'Approved by HOD of Department'
    VERIFIED_BY_DA = 'Verified by Dealing Assistant'
    APPROVED_BY_SrAO = 'Approved by Senior Audit Officer.'
    APPROVED_BY_AR = 'Approved by Assistant Registrar'
    APPROVED_BY_R = 'Approved by Registrar'
    AMOUNT_TRANSFERRED = 'Reimbursed'
    REJECTED_BY_HOD = 'Rejected by HOD of Department'
    REJECTED_BY_DA = 'Rejected by Dealing Assistant'
    REJECTED_BY_SrAO = 'Rejected by Senior Audit Officer.'
    REJECTED_BY_AR = 'Rejected by Assistant Registrar'
    REJECTED_BY_R = 'Rejected by Registrar'

    def __init__(self):
        pass
