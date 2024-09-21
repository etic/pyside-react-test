from react import *


@component
def Square(label, onSquareClick):
    return Button(text=label,
                  onClick=onSquareClick)

@component
def Board(xIsNext, squares, onPlay):
    def handleClick(i):
        if squares[i] or calculateWinner(squares):
            return
        nextSquares = squares.copy()
        nextSquares[i] = 'X' if xIsNext else 'O'
        onPlay(nextSquares)
    
    winner = calculateWinner(squares)
    if winner:
        status = 'Winner: ' + winner
    else:
        status = 'Next player: ' + ('X' if xIsNext else 'O')
    
    return BoxLayout(direction=BoxLayout.TopToBottom, children=[
        Label(text=status),
        BoxLayout(direction=BoxLayout.LeftToRight, children=[
            Square(squares[0], onSquareClick=lambda: handleClick(0)),
            Square(squares[1], onSquareClick=lambda: handleClick(1)),
            Square(squares[2], onSquareClick=lambda: handleClick(2)),
        ]),
        BoxLayout(direction=BoxLayout.LeftToRight, children=[
            Square(squares[3], onSquareClick=lambda: handleClick(3)),
            Square(squares[4], onSquareClick=lambda: handleClick(4)),
            Square(squares[5], onSquareClick=lambda: handleClick(5)),
        ]),
        BoxLayout(direction=BoxLayout.LeftToRight, children=[
            Square(squares[6], onSquareClick=lambda: handleClick(6)),
            Square(squares[7], onSquareClick=lambda: handleClick(7)),
            Square(squares[8], onSquareClick=lambda: handleClick(8)),
        ]),
    ])

@component
def Game():
    xIsNext, setXIsNext = useState(True)
    history, setHistory = useState([[None] * 9])
    currentMove, setCurrentMove = useState(0)
    currentSquares = history[currentMove]
    
    def handlePlay(nextSquares):
        nextHistory = history[:currentMove + 1] + [nextSquares]
        setHistory(nextHistory)
        setCurrentMove(len(nextHistory) - 1)
        setXIsNext(not xIsNext)
    
    def jumpTo(nextMove):
        setCurrentMove(nextMove)
        setXIsNext(nextMove % 2 == 0)
        
    def makeMove(move):
        if move > 0:
            description = 'Go to move #' + str(move)
        else:
            description = 'Go to game start'
        return Button(text=description, onClick=lambda: jumpTo(move))
    moves = list(map(makeMove, range(len(history))))
    
    return BoxLayout(direction=BoxLayout.LeftToRight, children=[
        Board(xIsNext=xIsNext, squares=currentSquares, onPlay=handlePlay),
        BoxLayout(direction=BoxLayout.TopToBottom, children=moves),
    ])

def calculateWinner(squares):
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for a, b, c in lines:
        if squares[a] and squares[a] == squares[b] and squares[a] == squares[c]:
            return squares[a]
    return None
    
window = Window()
window.render(Game())

