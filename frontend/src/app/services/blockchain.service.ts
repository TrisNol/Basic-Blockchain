import { Injectable } from '@angular/core';
import {HttpClient } from '@angular/common/http'
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BlockchainService {

  constructor(private http:HttpClient) {

   }

  public createTransaction(author: string, content: string): void{
    if(author != "" && content != ""){
      this.http.post(environment.backend+"/new_transaction", {author: author, content: content}, { responseType: 'text' })
        .subscribe(response => console.log(response))
    }
  }

  public mine(): void{
    this.http.get(environment.backend+"/mine", { responseType: 'text' })
      .subscribe(data => this.updateChain().subscribe())
  }

  public updateChain(): Observable<any>{
    return this.http.get(environment.backend+"/chain", { responseType: 'text' })
  }
}
