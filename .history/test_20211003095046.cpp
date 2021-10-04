#include <bits/stdc++.h>


class WBottle {
    public:
        string ma_loai;
        string ten_loai;
        int dung_tich;
        string ngay_san_xuat;

    private:

        int pt_tang_dung_tich(int d){
            dung_tich = dung_tich + d
            if (dung_tich<0){
                return 0;
            }
            else {
                return dung_tich
            }
        }
    
}

int main() {
    int n, k;
    WBottle A[1000];
    cin >> n >> k;
    for (int i=0; i<=n; i++){
        cin >> A[i].ma_loai >> A[i].ten_loai >> A[i].dung_tich >> A[i].ngay_san_xuat;
    }
    int max = A[n].pt_tang_dung_tich(k)
    for (int i=n-1; i<=0; i-- ){
        if(A[i].pt_tang_dung_tich(k) >= A[i].pt_tang_dung_tich(max)){
            max = i;
        }
    }
    cout << A[max].ten_loai << " " << A[max].ngay_san_xuat;
    cout << "{"

    return 0;
}