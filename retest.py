import pytest
from coverage import Coverage

if __name__ == "__main__":
    cov = Coverage()
    cov.start()
    pytest.main(["-vv", "--lf"])
    cov.stop()
    cov.save()
    cov.html_report(directory=".htmlcov", omit=["*/tests*"])
