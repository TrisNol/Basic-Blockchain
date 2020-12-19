import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BlockchainService {

  constructor(private http: HttpClient) {

  }

  public createTransaction(target: string, content: string): void {
    if (target != "" && content != "") {
      this.http.post(environment.backend + "/new_transaction", {target: target, content: content }, { responseType: 'text' })
        .subscribe(response => console.log(response))
    }
  }

  public mine(): void {
    this.http.get(environment.backend + "/mine", { responseType: 'text' })
      .subscribe(data => console.log(data))
  }

  public updateChain(): Observable<any> {
    return this.http.get(environment.backend + "/my_transactions", { responseType: 'text' })
  }
}
