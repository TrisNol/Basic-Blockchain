import { Component } from '@angular/core';
import { BlockchainService } from './services/blockchain.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'blockchain-frontend';

  author = "";
  content = "";

  transactions = []

  constructor(public blockchainService: BlockchainService) {

  }

  public sendToBlockchain() {
    this.blockchainService.createTransaction(this.author, this.content)
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
