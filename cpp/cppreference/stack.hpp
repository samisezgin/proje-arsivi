#pragma once
//#include <iostream>

struct node
{
    int *data;
    node *next;

    node() : data(new int(0))
    {
        std::cout << "constructed" << std::endl;
    }
    node(int data_) : data(new int(data_))
    {
        std::cout << "value constructed" << std::endl;
    }
    node(const node &node_)
    {
        this->data = new int;
        *this->data = *node_.data;
        std::cout << "copy constructed" << std::endl;
    }
    node(node &&node_)
    {
        this->data = node_.data;
        node_.data = nullptr;
        std::cout << "move constructed" << std::endl;
    }
    node &operator=(const node &node_)
    {
        this->data = new int;
        *this->data = *node_.data;
        std::cout << "copy assign" << std::endl;
        return *this;
    }
    node &operator=(node &&node_)
    {
        std::cout << "move assign" << std::endl;
        this->data = node_.data;
        node_.data = nullptr;
        return *this;
    }
    ~node()
    {
        if (data)
        {
            delete data;
        }
        std::cout << "destructed" << std::endl;
    }
};

template <typename _type>
class stack
{
public:
    using reference = typename _type &;
    using const_reference = typename const _type &;
    using pointer = typename _type *;

    void *block; //512 elements
    pointer root;
    pointer next_free;

    stack() : block(std::malloc(sizeof(_type) * 512)), root(nullptr), next_free(static_cast<pointer>(block))
    {
    }
    ~stack()
    {
        while (root)
        {
            pop();
        }
    }

    template <typename... _args>
    void push(_args &&...args_)
    {
        root = new (next_free) _type(std::forward<_args>(args_)...);
        ++next_free;
        print();
    }

    reference top()
    {
        return *root;
    }

    const_reference top() const
    {
        return *root;
    }

    void pop()
    {
        root->~_type();
        --next_free;
        if (root == static_cast<pointer>(block))
        {
            root = nullptr;
        }
        else
        {
            --root;
        }
        print();
    }

    void print()
    {
        std::cout<<"\t ----"<<std::endl;
        pointer seeker=root;
        while(seeker)
        {
            std::cout<<"\t"<<static_cast<void*>(seeker)<<std::endl;
            if(seeker==static_cast<pointer>(block))
            {
                return;
            }
            --seeker;
        }
        std::cout<<"\t ----"<<std::endl;
    }
};