import json
import sys
import os

# servicesへのパスを追加
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from services.sandbox_service import notebook_to_python


def test_notebook_to_python():
    nb = {
        "cells": [
            {"cell_type": "code", "source": "a = 1\nb = 2\nprint(a + b)", "metadata": {}},
            {"cell_type": "markdown", "source": "# Title", "metadata": {}},
            {"cell_type": "code", "source": "print('done')", "metadata": {}}
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 2,
    }
    nb_str = json.dumps(nb)
    code = notebook_to_python(nb_str)
    assert "a = 1" in code
    assert "print('done')" in code

