import os
from flask import Flask, request, redirect, url_for, render_template

import RegexFlask.FlaskPuzzleManager


def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    puzzle_manager = FlaskPuzzleManager.FlaskPuzzleManager()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/puzzle')
    def puzzle():
        col_clues = puzzle_manager.get_col_clues()
        row_clues = puzzle_manager.get_row_clues()
        return render_template('puzzle.html', hint=puzzle_manager.get_hint(),
                               colclue0=col_clues[0], colclue1=col_clues[1],
                               colclue2=col_clues[2], colclue3=col_clues[3],
                               colclue4=col_clues[4], rowclue0=row_clues[0],
                               rowclue1=row_clues[1], rowclue2=row_clues[2],
                               rowclue3=row_clues[3], rowclue4=row_clues[4],
                               more_premade=puzzle_manager.premade_remain())

    @app.route('/verify', methods=['POST', 'GET'])
    def verify():
        puzzle_manager.update(request)
        if puzzle_manager.check_puzzle():
            return redirect(url_for('correct'))
        else:
            return redirect(url_for('incorrect'))

    @app.route('/new_premade', methods=['POST', 'GET'])
    def new_premade():
        puzzle_manager.new_premade_puzzle()
        return redirect(url_for('puzzle'))

    @app.route('/new_random', methods=['POST', 'GET'])
    def new_random():
        puzzle_manager.new_random_puzzle()
        return redirect(url_for('puzzle'))

    @app.route('/correct')
    def correct():
        col_clues = puzzle_manager.get_col_clues()
        row_clues = puzzle_manager.get_row_clues()
        puzzle = puzzle_manager.get_puzzle()
        return render_template('correct.html', hint=puzzle_manager.get_hint(),
                               colclue0=col_clues[0], colclue1=col_clues[1],
                               colclue2=col_clues[2], colclue3=col_clues[3],
                               colclue4=col_clues[4], rowclue0=row_clues[0],
                               rowclue1=row_clues[1], rowclue2=row_clues[2],
                               rowclue3=row_clues[3], rowclue4=row_clues[4],
                               i00=puzzle[(0, 0)], i01=puzzle[(0, 1)], i02=puzzle[(0, 2)],
                               i03=puzzle[(0, 3)], i04=puzzle[(0, 4)],
                               i10=puzzle[(1, 0)], i11=puzzle[(1, 1)], i12=puzzle[(1, 2)],
                               i13=puzzle[(1, 3)], i14=puzzle[(1, 4)],
                               i20=puzzle[(2, 0)], i21=puzzle[(2, 1)], i22=puzzle[(2, 2)],
                               i23=puzzle[(2, 3)], i24=puzzle[(2, 4)],
                               i30=puzzle[(3, 0)], i31=puzzle[(3, 1)], i32=puzzle[(3, 2)],
                               i33=puzzle[(3, 3)], i34=puzzle[(3, 4)],
                               i40=puzzle[(4, 0)], i41=puzzle[(4, 1)], i42=puzzle[(4, 2)],
                               i43=puzzle[(4, 3)], i44=puzzle[(4, 4)],
                               more_premade=puzzle_manager.premade_remain())

    @app.route('/incorrect')
    def incorrect():
        return render_template('incorrect.html',
                               more_premade=puzzle_manager.premade_remain())

    return app
