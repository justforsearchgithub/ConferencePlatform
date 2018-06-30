def get_organization(user):
    if user.has_perm('account.OrganizationUser_Permission'):
        return user.organizationuser
    elif user.has_perm('account.OrganizationSubUser_Permission'):
        return user.organizationsubuser.organization
    else:
        return None