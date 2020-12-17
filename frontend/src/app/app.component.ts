import { Component } from '@angular/core';
import { Transaction } from './models/Transaction';
import { BlockchainService } from './services/blockchain.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'blockchain-frontend';

  transaction: Transaction =  {target: "", content: ""};

  transactions: Transaction[] = []

  constructor(public blockchainService: BlockchainService) {

  }

  public sendToBlockchain() {
    this.blockchainService.createTransaction(this.transaction.target, this.transaction.content)
  }

  public mine() {
    this.blockchainService.mine();
  }
  public updateChain() {
    this.transactions = []
    this.blockchainService.updateChain()
      .subscribe(data => {
        data = JSON.parse(data)
        data.chain.forEach(block => {
          block.transactions.forEach(
            transaction => this.transactions.push(transaction)
          )
        });
      });
  }
}
