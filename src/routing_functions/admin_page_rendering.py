from flask import Flask, render_template, request, redirect, url_for, json, Response, jsonify, make_response, flash
import logging

from src.models import *
from src.authentication import *
from src.image_handling import *

class AdminPageRendering():
   
    def permissions_requests_admin():
        if not check_if_admin(request):
            return redirect('/')
        requests = PermissionsRequest.query.filter_by(is_visible=True).order_by(PermissionsRequest.id).all()
        return render_template("permissions_request_admin.html", admin_token=True, prequests=requests, useraccount=get_account(request))

    def deny_request(requestid):
        if not check_if_admin(request):
            return redirect('/')
        permission_request = PermissionsRequest.query.get_or_404(requestid)
        permission_request.is_visible = False
        db.session.commit()
        return redirect('/permissions/requests/admin')

    def approve_request(requestid):
        if not check_if_admin(request):
            return redirect('/')
        permission_request = PermissionsRequest.query.get_or_404(requestid)
        permission_request.is_visible = False
        db.session.add(AccountPermission(permission_type=permission_request.permission_type, account_id=permission_request.account_id))
        db.session.commit()
        return redirect('/permissions/requests/admin')

    def uploadnewimage():
        if not check_if_admin(request):
            return redirect('/')
        image_id = uploadimage(request)
        return redirect('/')

