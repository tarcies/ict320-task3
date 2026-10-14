
@app.context_processor
def inject_user():
    print('')
    # global user, name, admin
    # return {'user': user, 'name': name, 'is_admin': admin}

@app.route('/')
@app.route('/<path:path>')
def f_default(path=None):
    print('')
    # if user:
    #     return redirect('/user/rentals')
    # return redirect('/auth/login')

@app.route('/auth/signup', methods=['GET', 'POST'])
def f_signup():
    print('')
    # global questions
    # if not questions: questions = getSecQ()
    
    # if request.method == 'POST':
    #     res, msg = signup(request.form, request.remote_addr);
    #     return render_template('auth/signup.html', questions=questions, res=res, msg=msg)
    
    # return render_template('auth/signup.html', questions=questions, res=True, msg='start')