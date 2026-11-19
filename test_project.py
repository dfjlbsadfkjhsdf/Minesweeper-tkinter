import project

def test_createBoard():
    assert project.createBoard(10, 10, 15) == 'Board created successfully'

def test_winEvent():
    assert project.winEvent() == 'Win window successfully created'

def test_main():
    assert project.main() == 'Main menu successfully created'
