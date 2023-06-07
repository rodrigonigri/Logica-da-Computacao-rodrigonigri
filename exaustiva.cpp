#include<iostream>
#include<vector>
#include<algorithm>
#include <random>
#include <stdlib.h>
#include <fstream>
#include<omp.h>
using namespace std;

#define RESET   "\033[0m"
#define BLACK   "\033[30m"      /* Black */
#define RED     "\033[31m"      /* Red */
#define GREEN   "\033[32m"      /* Green */
#define YELLOW  "\033[33m"      /* Yellow */
#define BLUE    "\033[34m"      /* Blue */
#define MAGENTA "\033[35m"      /* Magenta */
#define CYAN    "\033[36m"      /* Cyan */
#define WHITE   "\033[37m"      /* White */
#define BOLDBLACK   "\033[1m\033[30m"      /* Bold Black */
#define BOLDRED     "\033[1m\033[31m"      /* Bold Red */
#define BOLDGREEN   "\033[1m\033[32m"      /* Bold Green */
#define BOLDYELLOW  "\033[1m\033[33m"      /* Bold Yellow */
#define BOLDBLUE    "\033[1m\033[34m"      /* Bold Blue */
#define BOLDMAGENTA "\033[1m\033[35m"      /* Bold Magenta */
#define BOLDCYAN    "\033[1m\033[36m"      /* Bold Cyan */
#define BOLDWHITE   "\033[1m\033[37m"      /* Bold White */


struct filme {
    int id;
    int inicio;
    int fim;
    int categoria;
};


int main(){
    int numero_filmes;
    int numero_categorias;
    vector<filme> filmes; // vetor que armazena todos os filmes
    vector<filme> cronograma; // vetor que armazena os filmes que serao vistos no dia
    vector<int> maximo_categorias; // vetor que diz quantos filmes por categoria {'0',3,7,5,2}


    cin >> numero_filmes >> numero_categorias;


    maximo_categorias.push_back(0);

    int max;
    for(int i = 0; i < numero_categorias; i++){
        cin >> max;
        maximo_categorias.push_back(max);
    }

    

    int hora_inicio, hora_fim, cat;

    for(int i = 0; i < numero_filmes; i++){
        cin >> hora_inicio;
        cin >> hora_fim;
        cin >> cat;

        if(hora_fim == 0){
            hora_fim = 24;
        }

        if(hora_fim > hora_inicio){
            filmes.push_back({i, hora_inicio,hora_fim, cat});
        }
    }
    /* suppose there are 3 movies in filmes(all the options):
    000
    001
    010
    011
    100
    101
    110
    111
    */
    for(int i = 0; i < pow(2, filmes.size()); i++){
        // create a vector that will store all the movies that will be watched and return the best one
        vector<filme> temp;
        int total = 0;
        int categorias[5] = {0,0,0,0,0};
        for(int j = 0; j < filmes.size(); j++){
            if(i & (1 << j)){
                temp.push_back(filmes[j]);
                total += filmes[j].fim - filmes[j].inicio;
                categorias[filmes[j].categoria] += 1;
            }
        }
        bool flag = true;
        for(int j = 1; j < 5; j++){
            if(categorias[j] > maximo_categorias[j]){
                flag = false;
                break;
            }
        }
        if(flag){
            if(cronograma.size() == 0){
                cronograma = temp;
            }
            else if(total > cronograma.size()){
                cronograma = temp;
            }
        }
    }

    return 0;
}







