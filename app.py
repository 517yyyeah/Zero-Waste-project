from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 유저 정보 저장
users = {}

# 상품 정보
products = [
    {'id': 1, '이름': '롯데 아이시스', '가격': 4000, '재고': 10, '이미지': 'LOTTE Icis.jpg'},
    {'id': 2, '이름': 'OKF 옥수수수염차', '가격': 5000, '재고': 8, '이미지': 'OKF 옥수수수염차.jpg'},
    {'id': 3, '이름': 'OKF 현미차', '가격': 5000, '재고': 8, '이미지': 'OKF 현미차.jpg'},
    {'id': 4, '이름': '몽베스트 생수', '가격': 3000, '재고': 12, '이미지': '몽베스트 생수.jpg'},
    {'id': 5, '이름': '롯데 유산균 에이드', '가격': 6000, '재고': 6, '이미지': '롯데 유산균 에이드.jpg'},
    {'id': 6, '이름': '매실 음료', '가격': 5000, '재고': 10, '이미지': '매실 음료.jpg'},
    {'id': 7, '이름': '뽀로로 딸기맛', '가격': 4000, '재고': 10, '이미지': '뽀로로딸기맛.jpg'},
    {'id': 8, '이름': '뽀로로 우유맛', '가격': 4000, '재고': 10, '이미지': '뽀로로우유맛.jpg'},
    {'id': 9, '이름': '웅진 알로에 즙', '가격': 5000, '재고': 7, '이미지': '웅진 알로에 즙.jpg'},
    {'id': 10, '이름': '포카리 (병)', '가격': 5000, '재고': 9, '이미지': '포카리병.jpg'},
    {'id': 11, '이름': '포카리 (캔)', '가격': 5000, '재고': 9, '이미지': '포카리스캔.png'},
    {'id': 12, '이름': '혜태 배', '가격': 4000, '재고': 8, '이미지': '혜태 배.jpg'}
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    if username not in users:
        users[username] = {'points': 0}
    return jsonify({'success': True, 'points': users[username]['points']})

@app.route('/buy', methods=['POST'])
def buy():
    data = request.json
    username = data['username']
    product_id = data['product_id']
    pay_method = data['payment']

    if username not in users:
        return jsonify({'success': False, 'error': '사용자 로그인 필요'})

    for product in products:
        if product['id'] == product_id and product['재고'] > 0:
            product['재고'] -= 1
            return jsonify({'success': True, 'message': f'{pay_method} 결제 완료!'})

    return jsonify({'success': False, 'error': '재고 없음'})

@app.route('/recycle', methods=['POST'])
def recycle():
    username = request.json['username']
    if username in users:
        users[username]['points'] += 1
        return jsonify({'success': True, 'points': users[username]['points']})
    return jsonify({'success': False})

@app.route('/redeem', methods=['POST'])
def redeem():
    username = request.json['username']
    if username not in users:
        return jsonify({'success': False, 'message': '사용자 로그인 필요'})

   # 정확한 이름으로 교환 대상 찾기
    water = next((p for p in products if p['이름'] == '몽베스트 생수'), None)
    if not water or water['재고'] <= 0:
        return jsonify({'success': False, 'message': '몽베스트 생수 재고 없음'})

    if users[username]['points'] >= 20:
        users[username]['points'] -= 20
        water['재고'] -= 1
        return jsonify({
            'success': True,
            'message': '포인트 20점으로 몽베스트 생수 교환 완료!',
            'points': users[username]['points'],
            'stock': water['재고']
        })
    else:
        return jsonify({'success': False, 'message': '포인트 부족으로 교환 실패'})

@app.route('/ranking')
def ranking():
    sorted_users = sorted(users.items(), key=lambda item: item[1]['points'], reverse=True)
    rankings = [(username, data['points']) for username, data in sorted_users]
    return render_template('ranking.html', rankings=rankings)

if __name__ == '__main__':
    app.run(debug=True)


